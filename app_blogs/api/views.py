# from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from app_blogs.models import Comment, Category, Tags, Post
from .serializers import CommentSerializer, CategorySerializer, TagsSerializer, PostWriteSerializer, PostReadSerializer

from app_auth.api import permissions

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
    permission_classes = [IsAuthenticatedOrReadOnly]

    # @csrf_exempt ОТКЛЮЧЕНИЕ ПРОВЕРКИ CSRF TOKEN 
    #   (Или использовать header "X-CSRFToken" для POST PUT PATCH DELETE) 
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagsViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthor | IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostWriteSerializer
        return PostReadSerializer

    def create(self, request, *args, **kwargs):
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        post = write_serializer.save()

        # После сохранения — читающий сериализатор
        read_serializer = PostReadSerializer(post, context=self.get_serializer_context())
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    
    # Не актуален, так как get_serializer_context
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)