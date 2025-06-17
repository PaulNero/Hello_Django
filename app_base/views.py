from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


# Create your views here.
class AboutView(TemplateView):
    template_name = 'app_base/about.html'

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'app_base/index.html', context={'title': 'Home Page'})