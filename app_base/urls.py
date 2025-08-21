from django.urls import path
from .views import index, AboutView, contacts
from django.contrib import admin

from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularSwaggerView, 
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', contacts, name='contacts'),

    # DRF Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]