from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment

from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy,  reverse
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Min, Max, F
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.contrib.auth.decorators import login_required

# Create your views here.



class PostListView(ListView):
    model = Post
    template_name = 'app_blogs/posts_list.html'
    context_object_name = 'posts'
    # queryset = Post.objects.filter
    # queryset = Post.objects.filter(is_published=True)
    paginate_by = 10

    # def get_queryset(self):
    #     return (Post.objects
    #         .annotate(
    #             author_username=F('author__username'),
    #             author_image=F('author__image_url'),
    #             category__name=F('category__name'),
    #         )
    #         .value('pk', 'title', 'content', 'views', 'author_username', 'author_image_url', 'category_name', 'created_at', 'tags__name'))

class PostDetailView(DetailView):
    model = Post
    template_name = 'app_blogs/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'
    # queryset = Post.objects.filter(is_published=True)

    # Избежание race condition :TODO Реализовать подобное для всех подсчетов в будущем
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # F-выражение — это способ сказать «обнови поле относительно его текущего значения» прямо в SQL.
        self.object.views = F('views') + 1
        self.object.save(update_fields=['views'])
        self.object.refresh_from_db(fields=['views'])
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.object._meta.model_name
        return context

# @login_required
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'app_blogs/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts_list')
    pk_url_kwarg = 'pk'

    
    def form_valid(self, form):
        try: 
            res = super().form_valid(form)
            messages.success(self.request, f"Пост {self.object.pk} успешно удалён")
            return res
        except ProtectedError:
            messages.error(self.request, f"Пост {self.object.pk} нельзя удалить из связанных объектов")
            return super().form_invalid(form)

# @login_required
class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "app_blogs/post_create.html"
    # fields = ['title', 'content', 'status']
    # success_url = reverse_lazy('posts_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Пост успешно создан")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании поста")
        return super().form_invalid(form)

# @login_required
class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = "app_blogs/post_update.html"
    # fields = ['title', 'content', 'status']
    pk_url_kwarg = 'pk'
    # success_url = reverse_lazy('posts_list')


def posts_list_paginated(request):
        # Важна сортировка!
        all_posts_qs = Post.objects.order_by('-created_at')
        # 1. Создаем Paginator (10 постов на страницу)
        paginator = Paginator(all_posts_qs, 6)
        # 2. Получаем номер страницы из GET-параметра (?page=...)
        page_number = request.GET.get('page')
        # 3. Получаем объект Page для нужной страницы
        page_obj = paginator.get_page(page_number)
        # 4. Передаем объект Page в контекст
        context = {
            'posts': page_obj,
            'total_count': all_posts_qs.count()
            }
        return render(request, 'app_blogs/post_list_paginated.html', context)

        def get_queryset(self):
            # return post.objects.annotate(comments_count=Count('comments'))
            return (Post.objects
                # .filter(is_published=True)
                .select_related('author', 'category')
                .prefetch_related('tags'))


# @login_required
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "app_blogs/post_detail.html"
    # fields = ['content']
    # success_url = reverse_lazy('posts_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['post'] = post
        return context

    def form_valid(self, form):
        # Привязка комментария к посту
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})

    # :TODO потом разобраться, то что выше работает
    # post = get_object_or_404(Post, pk=self.kwargs['pk'])
    
    # form = CommentForm(request.POST)
    # if form.is_valid():
        # comment = form.save(commit=False)
        # comment.post = post
        # comment.save()
    #     return redirect('post_detail', pk=post.pk)

    # return redirect('post_detail', pk=post.pk')

# @require_POST
# def create_comment(request: HttpRequest, pk: int) -> HttpResponse:
#     post = get_object_or_404(Post, pk=pk)
#     post.comments.create(content=request.POST['content'])
#     return redirect('post_detail', pk=post.pk)

# @login_required
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'app_blogs/comment_confirm_delete.html'
    context_object_name = 'comment'
    success_url = reverse_lazy('posts_list')
        
    def form_valid(self, form):
        messages.success(self.request, "Комментарий успешно удалён")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

@login_required
def posts_stats(request:HttpRequest) -> HttpResponse:
    posts_stats = Post.objects.aggregate(
        total_posts=Count('pk'), # Общее количество постов
        # average_rating=Avg('rating'), # Средний рейтинг
        # min_rating=Min('rating'), # Минимальный рейтинг
        # max_rating=Max('rating'), # Максимальный рейтинг
        avg_views=Avg('views'),
        min_views=Min('views'),
        max_views=Max('views'),
        # avg_comments_on_post=Avg("comment__count"), # Среднее количество комментариев на пост
        avg_comments=Avg('comment'), 
        unique_posts_authors=Count('author', distinct=True) # Количество уникальных авторов
        )
    
    comment_stats = Comment.objects.aggregate(
        total_comments=Count("pk"),
        unique_comments_authors=Count('author', distinct=True),
        )
    posts_stats.update(comment_stats)
    return render(request, 'app_blogs/stats.html', context=posts_stats)
