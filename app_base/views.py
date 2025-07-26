from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'app_base/about.html'

@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'app_base/index.html', context={'title': 'Home Page'})

@login_required
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