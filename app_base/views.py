from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .forms import ContactForm
from django.contrib import messages

# Create your views here.
class AboutView(TemplateView):
    template_name = 'app_base/about.html'

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'app_base/index.html', context={'title': 'Home Page'})

def contacts(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            messages.success(request, "Заявка принята")
            return redirect('contacts')
        else:
            print(form.errors)
            messages.error(request, "Проверьте правильность заполнения формы")
            return render(request, "app_base/contacts.html", context={'form': form})

    context = {
        "title": "Contacts",
        "form": ContactForm()
    }

    return render(request, 'app_base/contacts.html', context=context)