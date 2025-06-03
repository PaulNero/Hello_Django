from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

profiles = {}

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', context={'title': 'Home Page'})

#TODO: Перенести в БД
user_data = {
    1: {
        'id': 1,
        'username':'Alex',
        'image_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fp0.piqsels.com%2Fpreview%2F156%2F222%2F449%2Fwomen-fashion-models-earring.jpg&f=1&nofb=1&ipt=c66ad45b672348d66e5917a07c2693c04207a10b5c41c452b4d27df993b3f052',
        'age': 30,
        'position': 'Software Engineer',
        'experience': 0.5,
        'hobbies': [],
        'tags': {},
        'email': 'example@example.com',
        'phone': '123-456-7890',
        'mobile': '987-654-3210',
        'address': {
            'street':'123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip': '12345'
        }
    },
    2: {
        'id': 2,
        'username':'Bob',
        'image_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fc.pxhere.com%2Fphotos%2Fda%2F92%2Fman_portrait_model_male_young_adult_attractive_guy-759715.jpg!d&f=1&nofb=1&ipt=32c890c989c27cd5fa661162c54c168a3824d0b6ed0323c2d462169141b281bb',
        'age': 25,
        'position': 'QA',
        'experience': 2,
        'hobbies': ['coding','reading','hiking'],
        'tags': {},
        'email': 'example@example.com',
        'phone': '123-456-7890',
        'mobile': '987-654-3210',
        'address': {
            'street':'123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip': '12345'
        }
    },
    3:{
        'id': 3,
        'username':'Paul',
        'image_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fget.pxhere.com%2Fphoto%2Fwork-man-working-person-people-white-alone-photo-looking-male-guy-meeting-standing-portrait-model-young-tie-student-fashion-business-clothing-lifestyle-modern-smiling-smile-shirt-education-collar-caucasian-cheerful-white-shirt-face-worker-happy-happiness-single-look-sexy-handsome-casual-attractive-adult-serious-stylish-sensual-confident-young-man-twenties-trendy-sleeve-masculine-user-hands-in-pocket-formal-wear-bussiness-man-office-style-1040941.jpg&f=1&nofb=1&ipt=870489924bee46e868a35613618a2dcc23a95c8df810b1e73feb53729412c4b1',
        'age': 25,
        'position': 'System Analyst',
        'experience': 5,
        'hobbies': ['coding','reading','hiking'],
        'tags': {},
        'email': 'example@example.com',
        'phone': '123-456-7890',
        'mobile': '987-654-3210',
        'address': {
            'street':'123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip': '12345'
        }
    },
}

def profile_user(request, user_id):
    if user_id not in user_data:
        return HttpResponseNotFound('User not found')
    
    context = {
        'user_data': user_data[user_id],
        'title': 'User Profile'
    }
    return render(request, 'user_profile.html', context)

def profiles_list(request):
    if len(user_data) == 0 in user_data:
        return HttpResponseNotFound('User not found')
    context = {
        'user_data': user_data,
        'user_count': len(user_data)
    }
    return render(request, 'users_all_profiles.html', context)
    