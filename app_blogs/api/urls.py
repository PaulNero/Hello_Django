from django.urls import path
from rest_framework.routers import DefaultRouter 
from .views import CommentViewSet

app_name = "api/blogs"

router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = router.urls




