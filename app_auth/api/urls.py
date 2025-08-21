from django.urls import path
from rest_framework.routers import DefaultRouter 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    )
from .views import (SessionAuthView, 
                    ObtainAuthTokenView, 
                    LogoutView, 
                    ProfileCreateView
    )


app_name = "api.auth"

router = DefaultRouter()

urlpatterns = router.urls + [
    # Session
    path('session_auth/', SessionAuthView.as_view(), name="session_auth"),
    # Token
    path('token_auth/', ObtainAuthTokenView.as_view(), name="token_auth"),
    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_jwt_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_jwt_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name="token_jwt_blacklist"),
    path('logout/', LogoutView.as_view(), name="token_jwt_logout"),
    # REGISTRATION
    path('registration/', ProfileCreateView.as_view(), name="profile_registration")
]




