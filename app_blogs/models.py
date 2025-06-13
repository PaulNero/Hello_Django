from django.db import models
from django.utils import timezone # Импортируем timezone
from django.urls import reverse

class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    author = models.ForeignKey('app_users.Profile', default=5, on_delete=models.SET_NULL ,null=True, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    tags =  models.ManyToManyField('Tags', related_name='posts')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self): 
        return f'{self.title}, {self.content[:20]}, {self.created_at.time()}'
    
    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs = {'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class Comment(models.Model): 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
                                related_name='comments', 
                                related_query_name='comment') 
    author = models.ForeignKey('app_users.Profile', default=5, on_delete=models.SET_NULL ,null=True, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

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
