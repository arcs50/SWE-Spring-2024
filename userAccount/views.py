from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from userAccount.admin import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# Create your views here.
from django.http import HttpResponse
from userAccount.models import Role

def index(request):
    return HttpResponse("Hello, world. You're at the recipeApp index.")    

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
def to_chef_role(request):
    if request.POST:
        obj, created = Role.objects.update_or_create(
            id=request.user.id,
            defaults={'id': request.user.id, 'role': 'C'}
        )
        return HttpResponse("You are a chef now.")
    else:
        return HttpResponse("something wrong")