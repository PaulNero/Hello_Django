from django.urls import path
from .views import index, AboutView, contacts
from django.contrib import admin

from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularSwaggerView, 
    SpectacularRedocView
)
from graphene_django.views import GraphQLView
from app_base.api.scheme import scheme

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', contacts, name='contacts'),

    # DRF Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # GraphQL
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=scheme)),
]