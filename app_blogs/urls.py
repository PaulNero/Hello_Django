from .views import PostDetailView, PostListView, PostDeleteView, PostCreateView, PostUpdateView, posts_list_paginated, CommentCreateView
from django.urls import path

urlpatterns = [
    # path('posts/', PostListView.as_view(), name='posts_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='blog_post_detail'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('posts/', posts_list_paginated, name='posts_list'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create')
    # path('post/<int:pk>/comment/', create_comment, name='comment_create')
]   