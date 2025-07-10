from rest_framework import serializers
from app_blogs.models import Comment, Category, Tags, Post
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializerDetail(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'image_url']

class PostSerializerDetail(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "title", "status"]

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializerDetail(read_only=True)
    post = PostSerializerDetail(read_only=True)
    # post_link = serializers.HyperLinkedIdentityField(
    #     view_name = 'post_detail',
    #     lookup_field = "pk",
    #     read_only = True
    # )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ["id", "title", "views", "created_at", "updated_at", "author", "post"]

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

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializerDetail(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ["id", "title", "views", "created_at", "updated_at", "author"]
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset = Post.objects.all(),
        #         fields = ['title', "content"]
        #     )
        # ]
    
    def validate_title(self, value):
        if 'spam' in value.lower():
            raise serializers.ValidationError("Title contains forbidden value")
        return value
        
    def validate(self, data):
        if 'test' in data['content'].lower():
            raise serializers.ValidationError("Title contains forbidden value")
        return data
