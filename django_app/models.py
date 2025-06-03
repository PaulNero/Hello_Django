from django.db import models

# Create your models here.
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    image_url = models.URLField(null=True)
    age = models.IntegerField(null=True)
    position = models.CharField(max_length=100, null=True)
    experience = models.FloatField(null=True)
    hobbies = models.JSONField(null=True)   
    tags = models.JSONField(null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    address = models.JSONField(null=True)
    social_links = models.JSONField(null=True)
    

