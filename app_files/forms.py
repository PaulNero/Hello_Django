# app_files/forms.py
from django import forms
from .models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
