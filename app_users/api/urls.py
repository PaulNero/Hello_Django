from django.urls import path
from rest_framework.routers import DefaultRouter 
from .views import ProfileViewSet

app_name = "api.users"

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profiles')

urlpatterns = router.urls




