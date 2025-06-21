from django.forms import fields, ModelForm, TextInput, Textarea, Select, SelectMultiple, Form, FileField, FileInput
from .models import Post, Comment

class PostForm(ModelForm):
        class Meta:
            model = Post
            fields = ("title", "content", "category", "tags", "status", )
            widgets = {
                "title": TextInput(attrs={'class': 'form-control'}),
                "content": Textarea(attrs={'class': 'form-control'}),
                "category": Select(attrs={'class': 'form-control'}),
                "tags": SelectMultiple(attrs={'class': 'form-control'}),
                "status": Select(attrs={'class': 'form-control'})
            }
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            "content": "Комментарий",
        }  