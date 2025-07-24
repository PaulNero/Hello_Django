# from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .filters import PostFilter

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

class DefaultPagination(LimitOffsetPagination):
    page_size = 10
    
    page_size_query_param = 'page_size'
    max_page_size = 20

    limit_query_param = "limit"
    offset_query_param = "offset"

    def paginate_queryset(self, queryset, request, view=None):
        # Метод задаёт self.limit, self.offset, self.count и self.request
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data): # Переопределение стандартного метода
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.count,
            'results': data
        })

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination

    filter_backends = [SearchFilter, OrderingFilter]
    
    # Фильтрация
    filterset_fields = ["post", "author"]

    # Поиск
    search_fields = ["content",
                    "=author__username", # Точное совпадение username автора
                    "^author__email"] # Поиск по email автора начинающегося с ...
    
    # Сортировка
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    

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
    pagination_classes = DefaultPagination


class TagsViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_classes = DefaultPagination


class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related('tags', 'category').select_related('author')
    # queryset = Post.objects.prefetch_related("category", "tags") TODO: Посмотреть работу
    permission_classes = [permissions.IsAuthor | IsAuthenticatedOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    
    # Фильтрация
    # filterset_fields = ["status"]
    filterset_class = PostFilter

    # Поиск
    search_fields = ["title", "content", 
                    "=author__username", # Точное совпадение username автора
                    "^author__email"] # Поиск по email автора начинающегося с ...
    
    # Сортировка
    ordering_fields = ['views', 'created_at']
    ordering = ['-created_at']


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