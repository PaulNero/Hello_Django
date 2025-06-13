from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy,  reverse
from django.core.paginator import Paginator






# Create your views here.
# def posts_list(request):
#     posts = Post.objects.filter(is_published=True)
#     return render(request, 'blog_app/posts_list.html', {'posts': posts})

# def blog_post_detail(request, post_id):
#     post = Post.objects.get(id=post_id)     
#     comments = Comment.objects.filter(post=post)
#     comments_count = len(Comment.objects.filter(post=post))
#     return render(request, 'blog_app/blog_post.html', {'post': post, 'comments': comments, 'comments_count': comments_count})

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    template_name = 'blog_app/posts_list.html'
    context_object_name = 'posts'
    # queryset = Post.objects.filter
    # queryset = Post.objects.filter(is_published=True)
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/blog_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'
    # queryset = Post.objects.filter(is_published=True)
    
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return self.object

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog_app/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts_list')
    pk_url_kwarg = 'pk'

class PostCreateView(CreateView):
    model = Post
    template_name = "blog_app/post_create.html"
    fields = ['title', 'content', 'is_published']
    # success_url = reverse_lazy('posts_list')

class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog_app/post_update.html"
    fields = ['title', 'content', 'is_published']
    pk_url_kwarg = 'pk'
    # success_url = reverse_lazy('posts_list')

def posts_list_paginated(request):
        # Важна сортировка!
        all_posts_qs = Post.published.filter(is_published=True).order_by('-created_at')
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
        return render(request, 'blog_app/post_list_paginated.html', context)

class CommentCreateView(CreateView):
    model = Comment
    template_name = "blog_app/blog_post.html"
    fields = ['content']
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
        return reverse('blog_post_detail', kwargs={'pk': self.kwargs['pk']})

# @require_POST
# def create_comment(request: HttpRequest, pk: int) -> HttpResponse:
#     post = get_object_or_404(Post, pk=pk)
#     post.comments.create(content=request.POST['content'])
#     return redirect('blog_post_detail', pk=post.pk)