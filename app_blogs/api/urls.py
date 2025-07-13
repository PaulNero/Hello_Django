from django.urls import path
from rest_framework.routers import DefaultRouter 
from .views import CommentViewSet, CategoryViewSet, TagsViewSet, PostViewSet

app_name = "api.blogs"

router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comments')
router.register('categories', CategoryViewSet, basename='categories')
router.register('tags', TagsViewSet, basename='tags')
router.register('posts', PostViewSet, basename='posts')

urlpatterns = router.urls




