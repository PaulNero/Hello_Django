# from rest_framework import generics
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.authtoken.models import Token
from .serializers import SessionAuthSerializer
from rest_framework.generics import CreateAPIView
from app_users.models import Profile
from app_users.api.serializers import ProfileRegistrationSerializer


# from .serializers import SessionSerializer

class SessionAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"status": "error", "detail": "Username and Password required."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        else:
            user = authenticate(username=username, password=password)
            if not user:
                return Response({"status": "Invalid credentials"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                # SessionID в Cookie
                login(request, user)
                return Response({"status": "success"}, 
                                status=status.HTTP_202_ACCEPTED)

    # def post(self, request):
    #     serializer = SessionAuthSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     username = serializer.validated_data["username"]
    #     password = serializer.validated_data["password"]

    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return Response({'status': "success"})
        
    #     return Response({"status": "error", "detail":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
class ObtainAuthTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"status": "error", "detail": "Username and Password required."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        else:
            user = authenticate(username=username, password=password)
            if not user:
                return Response({"status": "Invalid credentials"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                token, _ = Token.objects.get_or_create(user = user)
                return Response({"status": "Success", "token": token.key}, 
                            status=status.HTTP_202_ACCEPTED)
            
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out"}, status = status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileCreateView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileRegistrationSerializer

