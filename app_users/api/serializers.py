from rest_framework import serializers
from app_users.models import Profile

class ProfileRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("username", "email")

class ProfileRUDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("id", "first_name", "last_name", "username", "email", "sex", "image_url")

class ProfileFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        # exclude = ("password",)
        # fields = ("first_name", "last_name", "username", "email")