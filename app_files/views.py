from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy,  reverse
from django.shortcuts import render, redirect, get_object_or_404
from django_config.settings import MEDIA_ROOT
from django.forms import Form, FileField
from .forms import FileUploadForm
from app_blogs.views import PostDetailView



# def file_upload(request:HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_upload_file(request.FILES['file'])
#             return redirect('file_upload')
        
#         else:
#             form = UploadFileForm()
        
#     return render(request, 'app_files/file_upload.html', context={'form': form})

# return render(request, "",)
#     def handle_upload_file(f):
#         with open(MEDIA_ROOT / f.name, 'wb+') as destination:
#             for chunk in f.chunks():
#                 destination.write(chunk)
    
#     if request.method == "POST":
#         file = request.FILES['file']
#         handle_upload_file(file)
#         return redirect('file_upload')


#     return render(request, 'app_files/file_upload.html')

# class UploadFileForm(Form):
#     file = FileField(upload_to="media/")

def file_upload(request, model_name, object_id):
    print(model_name, object_id)
    if model_name in ['post', 'comment']:
        app_label = 'app_blogs'
    else:
        app_label = 'app_users'
    
    # content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name, pk=object_id)
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    model_class = content_type.model_class()
    obj = get_object_or_404(model_class, pk=object_id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.content_object = obj 
            file.save()
            return redirect(obj.get_absolute_url())
    else:
        form = FileUploadForm()

    return render(request, 'app_files/file_upload.html', {
        'form': form,
        'object': obj,
        'model_name': model_name,
        'object_id': object_id  
    })