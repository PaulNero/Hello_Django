from django.db import models
from django.utils import timezone # Импортируем timezone

class Post(models.Model):
    # Поля модели (соответствуют столбцам в таблице)
    title = models.CharField(max_length=200)
    # blank=True - поле необязательно для заполнения в формах
    content = models.TextField(blank=True)
    # Используем default
    created_at = models.DateTimeField(default=timezone.now)
    
    # Или auto_now_add=True (устанавливается при создании записи)
    # Обновляется при каждом сохранении записи
    updated_at = models.DateTimeField(auto_now=True)
    
    # Метод для строкового представления объекта

    def __str__(self):
        return self.title

    # Create your models here.
