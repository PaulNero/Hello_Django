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
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework.filters import OrderingFilter
from rest_framework import status
from app_auth.api.permissions import (IsOwnerOrStaff)

from rest_framework.decorators import action

from app_users.models import Profile
from .serializers import ProfileRUDSerializer, ProfilePasswordChangeSerializer, AdminPasswordChangeSerializer

# class ProfileViewSet(ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

class ProfileListView(ListAPIView):
    queryset = Profile.objects.all().order_by('username')
    serializer_class = ProfileRUDSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['username']

    @action(detail=False, methods=['get'])
    def recent_users(self, request):
        
        queryset = Profile.objects.all().order_by('-last_login')
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfileRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileRUDSerializer
    permission_classes = [IsOwnerOrStaff]

class ProfileChangePasswordViewSet(ModelViewSet):

    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrStaff]

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()

        if request.user == user:
            serializer = ProfilePasswordChangeSerializer(
                data=request.data, 
                context={'user': user, 'request': request}
            )
        
        elif request.user.is_staff:
            serializer = AdminPasswordChangeSerializer(
                data=request.data
            )
        
        else:
            return Response({
                "status": "error",
                "message": "Permission denied"
            }, status=status.HTTP_403_FORBIDDEN)
        
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            try:
                BlacklistedToken.objects.filter(token__user=user).delete()
            except Exception as e:
                print(f"Warning: Could not blacklist tokens for user {user.id}: {e}")

            return Response({
                'status': 'success',
                'message': 'Password changed successfully'
                }, status=status.HTTP_200_OK)
        
        
        return Response({
            'status': 'error',
            'errors': serializer.errors}
            , status=status.HTTP_400_BAD_REQUEST)
        
