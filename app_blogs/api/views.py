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

class TagsViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    # Не актуален, так как get_serializer_context
    # def rerform_create(self, serializer):
    #     serializer.save(author=self.request.user)