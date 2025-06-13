from django.db import models
from django.urls import reverse
from django.templatetags.static import static

# Create your models here.
class Profile(models.Model):
    
    class SexChoices(models.TextChoices):
        MALE = 'M', 'MALE'
        FEMALE = 'F', 'FEMALE'
        OTHER = 'O', 'OTHER'

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=False, unique=True)
    image_url = models.URLField(max_length=300, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(choices=SexChoices.choices, default=SexChoices.MALE)
    position = models.CharField(max_length=100, null=True, blank=True)
    experience = models.FloatField(null=True, blank=True)
    hobbies = models.JSONField(null=True, blank=True)   
    tags = models.JSONField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    mobile = models.CharField(max_length=20, null=True, blank=True, unique=True)
    address = models.JSONField(null=True, blank=True)
    social_links = models.JSONField(null=True, blank=True)
    password = models.CharField(max_length=128)
    role = models.CharField(default="user")

    def get_avatar_url(self):
        if self.image_url:
            return self.image_url
        elif self.sex == 'F':
            return static('img/default_woman_avatar.svg')
        else:
            return static('img/default_man_avatar.svg')