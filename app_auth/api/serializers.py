from rest_framework import serializers
from app_users.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class SessionAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class ProfileRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ("id", "username", "password")
        extra_kwargs = {
            "password": {"write_only": True}
            }
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Profile.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
