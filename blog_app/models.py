from django.db import models
from django.utils import timezone # Импортируем timezone

class Post(models.Model):
    # Поля модели (соответствуют столбцам в таблице)
    title = models.CharField(max_length=200)
    # blank=True - поле необязательно для заполнения в формах
    content = models.TextField(blank=True)

    author = models.ForeignKey('django_app.Profile', default=None, on_delete=models.SET_NULL ,null=True, max_length=200)
    # Используем default
    created_at = models.DateTimeField(default=timezone.now)
    
    # Или auto_now_add=True (устанавливается при создании записи)
    # Обновляется при каждом сохранении записи
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    # Метод для строкового представления объекта

    def __str__(self):
        return f'{self.title}, {self.content[:20]}, {self.created_at.time()}'

    # Create your models here.

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('django_app.Profile', default=None, on_delete=models.SET_NULL ,null=True, max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}, {self.content[:20]}, {self.created_at.time()}'