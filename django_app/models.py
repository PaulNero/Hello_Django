from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=False, default="Unusual Nickname")
    image_url = models.URLField(max_length=300, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    experience = models.FloatField(null=True, blank=True)
    hobbies = models.JSONField(null=True, blank=True)   
    tags = models.JSONField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    address = models.JSONField(null=True, blank=True)
    social_links = models.JSONField(null=True, blank=True)
    password = models.CharField(max_length=128, default=123123)
    role = models.CharField(default="user")
