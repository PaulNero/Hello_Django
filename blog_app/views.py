from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import TemplateView, ListView
from .models import Post




# Create your views here.
# def posts_list(request):
#     posts = Post.objects.filter(is_published=True)
#     return render(request, 'blog_app/posts_list.html', {'posts': posts})

def blog_post_detail(request, post_id):
    post = Post.objects.get(id=post_id)     
    comments = Comment.objects.filter(post=post)
    comments_count = len(Comment.objects.filter(post=post))
    return render(request, 'blog_app/blog_post.html', {'post': post, 'comments': comments, 'comments_count': comments_count})

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    template_name = 'blog_app/posts_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True)
    # queryset = Post.objects.filter(is_published=True)
    paginate_by = 10