# from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from app_blogs.models import Comment
from .serializers import CommentSerializer

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