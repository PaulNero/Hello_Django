from django.urls import path
from .views import index, AboutView, contacts
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', contacts, name='contacts'),
]