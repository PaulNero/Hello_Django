from django.urls import path
from rest_framework.routers import DefaultRouter 
# from .views import ProfileViewSet
from .views import ProfileListView, ProfileRUDView

app_name = "api.users"

router = DefaultRouter()
# router.register('profiles', ProfileViewSet, basename='profiles'),

urlpatterns = router.urls + [
    path('profiles/', ProfileListView.as_view(), name='profiles'),
    path('profiles/<int:pk>', ProfileRUDView.as_view(), name='profiles_actions')
]

# app_name = "api.auth"

# router = DefaultRouter()

# urlpatterns = router.urls + [
#     # Session
#     path('session_auth/', SessionAuthView.as_view(), name="session_auth"),
#     # Token
#     path('token_auth/', ObtainAuthTokenView.as_view(), name="token_auth"),
#     # JWT
#     path('token/', TokenObtainPairView.as_view(), name='token_jwt_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_jwt_refresh'),
#     path('token/blacklist/', TokenBlacklistView.as_view(), name="token_jwt_blacklist"),
#     path('logout/', LogoutView.as_view(), name="token_jwt_logout"),
#     # REGISTRATION
#     path('registration/', ProfileCreateView.as_view(), name="profile_registration"),
# ]


