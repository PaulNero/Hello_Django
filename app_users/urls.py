from django.urls import path, register_converter, converters
from .views import UserDetailView, UserUpdateView, UserCreateView, UserDeleteView, users_list_paginated, UserLoginView
from django.contrib.auth.views import LogoutView


# from django.conf import settings
# from django.conf.urls.static import static

# class YearConverter:
#     regex = '[0-9]{4}'
    
#     def to_python(self, value):
#         return int(value)
    
#     def to_url(self, value):
#         return str(value)

# register_converter(converters.YearConverter, 'year')

# urlpatterns = [
#     path('profiles', profiles_list, name='profiles_list'),
#     path('profile/<int:user_id>/', profile_user, name='profile_user'),
# ]

app_name = "users"

urlpatterns = [
    # path('profiles', UsersListView.as_view(), name='profiles_list'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile_user'),
    path('profile/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('profile/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('profile/create/', UserCreateView.as_view(), name='user_registration'),
    path('profiles', users_list_paginated, name='profiles_list'),
    path('login', UserLoginView.as_view(), name='user_login'),
    path('logout', LogoutView.as_view(), name='user_logout'),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)