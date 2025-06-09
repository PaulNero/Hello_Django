from django.urls import path, register_converter, converters
# from .views import index, profile_user, profiles_list 
from .views import index, UsersListView, UserDetailView, UserUpdateView, UserCreateView

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

urlpatterns = [
    path('profiles', UsersListView.as_view(), name='profiles_list'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile_user'),
    path('profile/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('profile/create/', UserCreateView.as_view(), name='user_registration'),
]