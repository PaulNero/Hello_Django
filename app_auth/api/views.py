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
from .serializers import ProfileRegistrationSerializer


# from .serializers import SessionSerializer

class SessionAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({
                "status": "error", 
                "message": "Username and Password required."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            user = authenticate(username=username, password=password)
            if not user:
                return Response({
                    "status": "error", 
                    "message": "Invalid credentials"
                    }, status=status.HTTP_401_UNAUTHORIZED)
            
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
            return Response({
                "status": "error", 
                "message": "Username and Password required."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            user = authenticate(username=username, password=password)
            if not user:
                return Response({
                    "status": "error",
                    "message": "Invalid credentials"
                    }, status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                token, _ = Token.objects.get_or_create(user = user)
                return Response({
                    "status": "Success", 
                    "token": token.key
                    }, status=status.HTTP_202_ACCEPTED)
            
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message": "Successfully logged out"
                }, status = status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({
                "message": "Error logging out",
                "detail": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileCreateView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            if Profile.objects.filter(username__iexact=username).exists():
                return Response({
                    "status": "error", 
                    "message": "User with this username already exists"
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            try: 
                user = serializer.save()
                # send_verification_email(user)        

                return Response({
                    "status": "success",
                    "message": "User created successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username
                    }
                }, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": "Error creating user", 
                    "detail": str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response({
            "status": "error", 
            "message": "Validation error",
            "detail": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

