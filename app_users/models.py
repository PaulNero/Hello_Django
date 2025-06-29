from django.db import models
from django.urls import reverse
from django.templatetags.static import static
from app_files.models import File
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(AbstractUser):

    USER_SEX_CHOICES = (
        ("M", "MALE"),
        ("F", "FEMALE"),
        ("O", "OTHER")
    )

    id = models.AutoField(primary_key=True)
    # user = models.OneToOneField('auth.User', on_delete=models.PROTECT, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, null=False, unique=True)
    image_url = models.URLField(max_length=300, null=True, blank=True)
    # files = GenericRelation(File) TODO: Нужно заменить image_url на files, что бы правильно работать с файлами
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(choices=USER_SEX_CHOICES, default=USER_SEX_CHOICES[0][0])
    position = models.CharField(max_length=100, null=True, blank=True)
    experience = models.FloatField(null=True, blank=True)
    hobbies = models.JSONField(null=True, blank=True)   
    tags = models.JSONField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    mobile = models.CharField(max_length=20, null=True, blank=True, unique=True)
    address = models.JSONField(null=True, blank=True)
    social_links = models.JSONField(null=True, blank=True)
    role = models.CharField(default="user")

    def __str__(self):
        return self.username

    def get_avatar_url(self):
        if self.image_url:
            return self.image_url
        elif self.sex == 'F':
            return static('img/default_woman_avatar.svg')
        else:
            return static('img/default_man_avatar.svg')

    # def get_avatar_url(self):
    #     if self.files:
    #         return self.files
    #     elif self.sex == 'F':
    #         return static('img/default_woman_avatar.svg')
    #     else:
    #         return static('img/default_man_avatar.svg')

    def get_absolute_url(self):
        return reverse('user_profile', kwargs = {'pk': self.pk})
        