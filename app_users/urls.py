from django.urls import path, register_converter, converters, reverse_lazy
from .views import UserDetailView, UserUpdateView, UserCreateView, UserDeleteView, users_list_paginated, UserLoginView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


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
#     path('profile/<int:user_id>/', user_profile, name='user_profile'),
# ]

app_name = "users"

urlpatterns = [
    # USERS ACTION
    # path('profiles', UsersListView.as_view(), name='profiles_list'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user_profile'),
    path('profile/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('profile/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('profile/create/', UserCreateView.as_view(), name='user_registration'),
    path('profiles', users_list_paginated, name='profiles_list'),

    # LOGIN
    path('login', UserLoginView.as_view(), name='user_login'),
    path('logout', LogoutView.as_view(), name='user_logout'),


    # PASSWORD RESET
    path('password_reset', PasswordResetView.as_view(
        template_name="app_users/user_password_reset.html",
        success_url=reverse_lazy('users:user_password_reset_done'),
        email_template_name="app_users/user_password_reset_email.html",
    ), name="user_password_reset"),
    
    path('password_reset/done', PasswordResetDoneView.as_view(
        template_name="app_users/user_password_reset_done.html",
    ), name='user_password_reset_done'),
    
    path('password_reset/confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(
        template_name='app_users/user_password_reset_confirm.html',
        success_url = reverse_lazy("users:user_password_reset_complete"),
    ), name='user_password_reset_confirm'),
    
    path('password_reset/complete', PasswordResetCompleteView.as_view(
        template_name="app_users/user_password_reset_complete.html",
    ), name="user_password_reset_complete"),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)