from rest_framework import serializers
from app_users.models import Profile
from django.contrib.auth.password_validation import validate_password

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

# class ProfilePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = Profile
#         fields = ("password")
#         extra_kwargs = {
#             "password": {"write_only": True}
#             }
        
#     def update(self, instance, validated_data):
#         password = validated_data.pop("password", None)
        
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
        
#         if password:
#             instance.set_password(password)
        
#         instance.save()
#         return instance

class ProfilePasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    repeat_password = serializers.CharField(required=True)


    def validate(self, data):
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("User not found")
        
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError("Old password is not correct")
        
        if data['new_password'] != data['repeat_password']:
            raise serializers.ValidationError("New passwords do not match")
        
        return data
    
class AdminPasswordChangeSerializer(serializers.Serializer):

    new_password = serializers.CharField(required=True, validators=[validate_password])
    repeat_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['repeat_password']:
            raise serializers.ValidationError("New passwords do not match")
        
        return data