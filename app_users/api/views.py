# from rest_framework import generics
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView, # GET LIST
    RetrieveAPIView, # GET ONE
    UpdateAPIView, # PUT | PATCH
    DestroyAPIView, # DELETE
    RetrieveUpdateAPIView, # GET ONE / PUT / PATCH
    RetrieveUpdateDestroyAPIView # GET ONE / PUT / PATCH / DELETE
    )
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import status
from app_auth.api.permissions import (IsOwnerOrStaff)

from app_users.models import Profile
from .serializers import ProfileRUDSerializer

# class ProfileViewSet(ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileRUDSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProfileRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileRUDSerializer
    permission_classes = [IsOwnerOrStaff]
