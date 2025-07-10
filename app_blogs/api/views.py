# from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from app_blogs.models import Comment, Category, Tags, Post
from .serializers import CommentSerializer, CategorySerializer, TagsSerializer, PostSerializer

# class CommentList(generics.ListAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

# class CommentCreate(generics.CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = []

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def rerform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def rerform_create(self, serializer):
        serializer.save(author=self.request.user)

class TagsViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

    def rerform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def rerform_create(self, serializer):
        serializer.save(author=self.request.user)