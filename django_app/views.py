from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy,  reverse 
from .models import Profile

profiles = {}

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', context={'title': 'Home Page'})

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



# def profile_user(request, user_id):
#     if not user_data:
#         return HttpResponseNotFound('User not found')
    
#     context = {
#         'user_data': user_data[user_id],
#         'title': 'User Profile'
#     }
#     return render(request, 'django_app/user_profile.html', context)

# def profiles_list(request):
#     if len(user_data) == 0 in user_data:
#         return HttpResponseNotFound('User not found')
#     context = {
#         'user_data': user_data,
#         'user_count': len(user_data)
#     }
#     return render(request, 'django_app/users_all_profiles.html', context)
    

class UsersListView(ListView):
    model = Profile
    template_name = 'django_app/users_all_profiles.html'
    context_object_name = 'users_data'
    paginate_by = 10

class UserDetailView(DetailView):
    model = Profile
    template_name = 'django_app/user_profile.html'
    context_object_name = 'user_data'
    pk_url_kwarg = 'pk'
    # queryset = Post.objects.filter(is_published=True)


class UserDeleteView(DeleteView):
    model = Profile
    template_name = 'django_app/user_delete.html'
    context_object_name = 'user_data'
    success_url = reverse_lazy('profiles_list')
    pk_url_kwarg = 'pk'

class UserCreateView(CreateView):
    model = Profile
    template_name = "django_app/user_registration.html"
    fields = ['first_name', 
                'last_name', 
                'nickname', 
                'image_url',
                'age',
                'position',
                'experience',
                'email',
                'phone',
                'mobile',
                'address',
                'password']
    # success_url = reverse_lazy('posts_list')
    def get_success_url(self):
        return reverse_lazy('profile_user', args=[self.object.pk])

class UserUpdateView(UpdateView):
    model = Profile
    template_name = "django_app/user_update.html"
    fields = ['first_name', 
                'last_name', 
                'nickname', 
                'image_url',
                'age',
                'position',
                'experience',
                'email',
                'phone',
                'mobile',
                'address',
                'password']
    pk_url_kwarg = 'pk'
    def get_success_url(self):
        return reverse_lazy('profile_user', args=[self.object.pk])
    
    

# def posts_list_paginated(request):
#         # Важна сортировка!
#         all_posts_qs = Profile.published.filter(is_published=True).order_by('-created_at')
#         # 1. Создаем Paginator (10 постов на страницу)
#         paginator = Paginator(all_posts_qs, 3)
#         # 2. Получаем номер страницы из GET-параметра (?page=...)
#         page_number = request.GET.get('page')
#         # 3. Получаем объект Page для нужной страницы
#         page_obj = paginator.get_page(page_number)
#         # 4. Передаем объект Page в контекст
#         context = {'posts': page_obj}
#         return render(request, 'blog_app/post_list_paginated.html', context)