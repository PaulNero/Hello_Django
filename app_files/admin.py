from django.contrib import admin
from django.utils.html import format_html

from .models import File
# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["id", "file", "object_id", "content_type_id", "file_image"]

    def file_image(self, obj):
        if obj.file.url.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return format_html('<img src="{}" style="max-height: 50px;">', obj.file.url)
        return "—"
    
    file_image.short_description = "Превью"