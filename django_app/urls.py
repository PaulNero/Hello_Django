from django.urls import path, register_converter, converters
from .views import index, profile_user, profiles_list 


# class YearConverter:
#     regex = '[0-9]{4}'
    
#     def to_python(self, value):
#         return int(value)
    
#     def to_url(self, value):
#         return str(value)

# register_converter(converters.YearConverter, 'year')

urlpatterns = [
    path('profiles', profiles_list, name='profiles_list'),
    path('profile/<int:user_id>/', profile_user, name='profile_user'),
]