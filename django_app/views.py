from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', context={'title': 'Home Page'})

def profile(request: HttpRequest, profile_id: int) -> HttpResponse:
    return render(request, 'profile.html', context={'title': 'Profile Page', 'profile_id': profile_id})