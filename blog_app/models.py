from django.db import models
from django.utils import timezone # Импортируем timezone
from django.urls import reverse

class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

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
    views = models.PositiveIntegerField(default=0)

    published = PublishedManager()
    
    # Метод для строкового представления объекта

    def __str__(self): 
        return f'{self.title}, {self.content[:20]}, {self.created_at.time()}'
    
    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs = {'pk': self.pk})

    # Create your models here.

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    

class Comment(models.Model): 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
                                related_name='comments', 
                                related_query_name='comment') 
    author = models.ForeignKey('django_app.Profile', default=None, on_delete=models.SET_NULL ,null=True, max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}, {self.content[:20]}, {self.created_at.time()}'
    
    class Meta:
        ordering = ['-created_at']