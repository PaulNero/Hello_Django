from rest_framework import serializers
from app_users.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class SessionAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
