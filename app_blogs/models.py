from django.db import models
from django.utils import timezone # Импортируем timezone
from django.urls import reverse
from app_files.models import File
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model

User = get_user_model()

# class PublishedManager(models.Manager):

#     def get_queryset(self):
#         return super().get_queryset().filter(is_published=True)

class TimeStampedModel (models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(TimeStampedModel):

    POST_STATUS_CHOICES = (
        ("draft", "Draft"), # Черновик
        ("published", "Published"), # Опубликовано
        ("un_published", "Un_published"), # Снято с публикации автором, не отображается в общей ленте, но видно в профиле автора
        ("archived", "Archived"), # Снято с публикации автором, видно только автору
        ("on_moderation", "On_moderation"), # Пост с низким рейтингом или на пост поступили жалобы, скрыт из общей ленты, отображается только автору и пользователям с возможностью модерации
        ("approved", "Approved"), # Пост возвращён с модерации, и отображается в общей ленте
        ("not_approved", "not_approved"), # Пост удалён пользователем с возможностью модерации, отображается только название поста, виден только автору поста
        ("deleted", "Deleted") # Пост удалён автором, отображается только название поста
    )

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL , null=True, related_name='posts')
    files = GenericRelation(File, related_query_name='posts', blank=True, null=True)
    # is_published = models.BooleanField(default=True)
    status = models.CharField(choices=POST_STATUS_CHOICES, default=POST_STATUS_CHOICES[0][0])
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    tags =  models.ManyToManyField('Tags', related_name='posts')

    objects = models.Manager()
    # published = PublishedManager()

    def __str__(self): 
        return f'{self.title}, {self.content[:20]}, {self.created_at.time()}'
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs = {'pk': self.pk})

    def get_url(self):
        return self.files.url

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class Comment(TimeStampedModel): 
    post = models.ForeignKey(Post, on_delete=models.PROTECT, 
                                related_name='comments', 
                                related_query_name='comment') 
    author = models.ForeignKey(User, on_delete=models.SET_NULL ,null=True, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return f'{self.author}, {self.content[:20]}, {self.created_at.time()}'
    
    class Meta:
        ordering = ['-created_at']
        
class Category(models.Model):
    
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        
# class PostTags(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
