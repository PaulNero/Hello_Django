from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy,  reverse 
from .models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .forms import CreateUserForm


profiles = {}

# #TODO: Перенести в БД
# user_data = {
#     1: {
#         'id': 1,
#         'first_name': 'Alex',
#         'last_name': 'First',
#         'image_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fp0.piqsels.com%2Fpreview%2F156%2F222%2F449%2Fwomen-fashion-models-earring.jpg&f=1&nofb=1&ipt=c66ad45b672348d66e5917a07c2693c04207a10b5c41c452b4d27df993b3f052',
#         'age': 30,
#         'position': 'Software Engineer',
#         'experience': 0.5,
#         'hobbies': [],
#         'tags': {},
#         'email': 'example@example.com',
#         'phone': '123-456-7890',
#         'mobile': '987-654-3210',
#         'address': {
#             'street':'123 Main St',
#             'city': 'Anytown',
#             'state': 'CA',
#             'zip': '12345'
#         },
#         'social_links': {
#             'website': 'https://example.com',
#             'github': 'https://github.com/example',
#             'twitter': 'https://twitter.com/example',
#             'linkedIn': 'https://www.linkedin.com/in/example',
#             'facebook': 'https://www.facebook.com/example',
#             'instagram': 'https://www.instagram.com/example',
#             'telegram': 'https://t.me/example'
#         }
#     },
#     2: {
#         'id': 2,
#         'first_name': 'John',
#         'last_name': 'Second',
#         'image_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fc.pxhere.com%2Fphotos%2Fda%2F92%2Fman_portrait_model_male_young_adult_attractive_guy-759715.jpg!d&f=1&nofb=1&ipt=32c890c989c27cd5fa661162c54c168a3824d0b6ed0323c2d462169141b281bb',
#         'age': 25,
#         'position': 'QA',
#         'experience': 2,
#         'hobbies': ['coding','reading','hiking'],
#         'tags': {},
#         'email': 'example@example.com',
#         'phone': '123-456-7890',
#         'mobile': '987-654-3210',
#         'address': {
#             'street':'123 Main St',
#             'city': 'Anytown',
#             'state': 'CA',
#             'zip': '12345'
#         },
#         'social_links': {
#             'website': 'https://example.com',
#             'github': 'https://github.com/example',
#             'twitter': 'https://twitter.com/example',
#             'linkedIn': 'https://www.linkedin.com/in/example',
#             'facebook': 'https://www.facebook.com/example',
#             'instagram': 'https://www.instagram.com/example',
#             'telegram': 'https://t.me/example'
#         }
#     },
#     3:{
#         'id': 3,
#         'first_name': 'Paul',
#         'last_name': 'Third',
#         'image_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fget.pxhere.com%2Fphoto%2Fwork-man-working-person-people-white-alone-photo-looking-male-guy-meeting-standing-portrait-model-young-tie-student-fashion-business-clothing-lifestyle-modern-smiling-smile-shirt-education-collar-caucasian-cheerful-white-shirt-face-worker-happy-happiness-single-look-sexy-handsome-casual-attractive-adult-serious-stylish-sensual-confident-young-man-twenties-trendy-sleeve-masculine-user-hands-in-pocket-formal-wear-bussiness-man-office-style-1040941.jpg&f=1&nofb=1&ipt=870489924bee46e868a35613618a2dcc23a95c8df810b1e73feb53729412c4b1',
#         'age': 25,
#         'position': 'System Analyst',
#         'experience': 5,
#         'hobbies': ['coding','reading','hiking'],
#         'tags': {},
#         'email': 'example@example.com',
#         'phone': '123-456-7890',
#         'mobile': '987-654-3210',
#         'address': {
#             'street':'123 Main St',
#             'city': 'Anytown',
#             'state': 'CA',
#             'zip': '12345'
#         },
#         'social_links': {
#             'website': 'https://example.com',
#             'github': 'https://github.com/example',
#             'twitter': 'https://twitter.com/example',
#             'linkedIn': 'https://www.linkedin.com/in/example',
#             'facebook': 'https://www.facebook.com/example',
#             'instagram': 'https://www.instagram.com/example',
#             'telegram': 'https://t.me/example'
#         }
#     },
# }



# def user_profile(request, user_id):
#     if not user_data:
#         return HttpResponseNotFound('User not found')
    
#     context = {
#         'user_data': user_data[user_id],
#         'title': 'User Profile'
#     }
#     return render(request, 'app_users/user_profile.html', context)

# def profiles_list(request):
#     if len(user_data) == 0 in user_data:
#         return HttpResponseNotFound('User not found')
#     context = {
#         'user_data': user_data,
#         'user_count': len(user_data)
#     }
#     return render(request, 'app_users/users_all_profiles.html', context)

class UserProfileRouterView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:user_login')
        
        if pk == request.user.pk:
            return redirect('users:user_logged')
        
        return redirect('users:user_profile', pk=pk)

class UserDetailView(DetailView):
    model = Profile
    template_name = 'app_users/user_profile.html'
    context_object_name = 'user_data'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.object._meta.model_name
        return context
    
class CurrentUserDetailView(UserDetailView):
    template_name = 'app_users/user_logged_profile.html'

    def get_object(self):
        return self.request.user

class UsersListView(ListView):
    model = Profile
    template_name = 'app_users/users_all_profiles.html'
    context_object_name = 'users_data'
    paginate_by = 10

class UserCreateView(CreateView):
    template_name = "app_users/user_registration.html"
    form_class = CreateUserForm
    success_url = reverse_lazy('users:user_login')

    def form_valid(self, form):
        res = super().form_valid(form)
        # self.object.set_password(self.object.password)
        # self.object.save()
        messages.success(self.request, "Пользователь успешно создан")
        return res



class UserDeleteView(DeleteView):
    model = Profile
    template_name = 'app_users/user_delete.html'
    context_object_name = 'user_data'
    success_url = reverse_lazy('users:profiles_list')
    pk_url_kwarg = 'pk'

# class UserCreateView(CreateView):
#     model = Profile
#     template_name = "app_users/user_registration.html"
#     fields = ['first_name', 
#                 'last_name', 
#                 'username', 
#                 'image_url',
#                 'age',
#                 'position',
#                 'experience',
#                 'email',
#                 'phone',
#                 'mobile',
#                 'address',
#                 'password']
#     # success_url = reverse_lazy('posts_list')
#     def get_success_url(self):
#         return reverse_lazy('users:user_profile', args=[self.object.pk])

class UserUpdateView(UpdateView): # TODO Изменить логику изменения данных пользователя только самим пользователем
    model = Profile
    template_name = "app_users/user_update.html"
    fields = ['first_name', 
                'last_name', 
                'username', 
                'image_url',
                'age',
                'position',
                'experience',
                'email',
                'phone',
                'mobile',
                'address']
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('users:user_profile', args=[self.object.pk])
    
class UserPasswordChangeView(PasswordChangeView):
    template_name = 'app_users/user_password_change.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Пароль успешно изменён.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:user_profile', args=[self.request.user.pk])

def users_list_paginated(request):
        # Важна сортировка!
        all_users_qs = Profile.objects.order_by('username')
        # 1. Создаем Paginator (10 постов на страницу)
        paginator = Paginator(all_users_qs, 6)
        # 2. Получаем номер страницы из GET-параметра (?page=...)
        page_number = request.GET.get('page')
        # 3. Получаем объект Page для нужной страницы
        page_obj = paginator.get_page(page_number)
        # 4. Передаем объект Page в контекст
        context = {
            'users_data': page_obj,
            'total_count': all_users_qs.count()
            }
        return render(request, 'app_users/users_list_paginated.html', context)

# def user_login(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = AuthenticationForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None and user.is_active:
#                 login(request, user)
#                 messages.success(request, "login successfull")
#                 return redirect('index')
#             else:
#                 messages.error(request, "login unsuccessable")

#             # user = form.save()
#             # return redirect('index')
#     else:
#         form = AuthenticationForm()
#         return render(request, 'app_users/user_login.html', context={'form': form})
    
# @login_required
# def user_logout(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         logout(request)
#     return redirect("user_login")

class UserLoginView(LoginView):
    template_name = "app_users/user_login.html"




