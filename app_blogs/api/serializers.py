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
    # post = PostSerializerDetail(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    # post_link = serializers.HyperLinkedIdentityField(
    #     view_name = 'post_detail',
    #     lookup_field = "pk",
    #     read_only = True
    # )

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ["id", "views", "created_at", "updated_at"]

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

class PostWriteSerializer(serializers.ModelSerializer):
    # author = AuthorSerializerDetail(read_only=True)
    # category = CategorySerializer(many=True)
    # tags = TagsSerializer(many=True)
    # comments = CommentSerializer(many=True, read_only=True)

    category = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    # author = AuthorSerializerDetail(read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
        read_only_fields = ["id", "views", "created_at", "updated_at", "author"]
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
    
    def create(self, validated_data):
        category_name = validated_data.pop("category")
        tag_names = validated_data.pop("tags")
        user = self.context["request"].user
        # validated_data['author'] = self.context['request'].user

        category, _ = Category.objects.get_or_create(name=category_name)
        post = Post.objects.create(author=user, category = category, **validated_data)

        for tag_name in tag_names:
            tag, _ = Tags.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        # return super().create(validated_data)
        return post

class PostReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagsSerializer(many=True)
    author = AuthorSerializerDetail()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'