from rest_framework import serializers
from app_blogs.models import Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

# class CommentSerializer(serializers.Serializer):
#     id = serializers.IntegerField(
#         read_only=True)
#     email = serializers.EmailField(required=True)
#     content = serializers.CharField(max_lenght=1000,
#                                     style={'base_template': 'textarea.html'})
#     created = serializers.DateTimeField(read_only=True)
#     post_id = serializers.IntegerField(required=True, write_only=True)

#     def validate_content(self, value):
#         if 'spam' in value.lower():
#             raise serializers.ValidationError(
#                 "Комментарий содержит плохое слово."
#             )
#         return value
