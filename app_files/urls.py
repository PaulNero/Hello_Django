from .views import file_upload
from django.urls import path

urlpatterns = [
    # path('/file_upload', file_upload, name='file_upload'),
    path('upload/<str:model_name>/<int:object_id>/', file_upload, name='file_upload'),
]   