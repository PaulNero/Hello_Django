from .views import blog_post_detail, PostListView
from django.urls import path

urlpatterns = [
    # path('posts', posts_list, name='posts_list'),
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('post/<int:post_id>/', blog_post_detail, name='blog_post_detail')
]   