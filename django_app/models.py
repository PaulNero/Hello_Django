from django.db import models

# Create your models here.
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    age = models.IntegerField(null=True)
    experience = models.FloatField(null=True)
    hobbies = models.JSONField(null=True)   
    tags = models.JSONField(null=True)
    address = models.JSONField(null=True)

