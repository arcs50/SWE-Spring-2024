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
        user = request.user
        chef_role, created = Role.objects.get_or_create(role='C', defaults={'role': 'Chef'})
        if chef_role not in user.role.all():
            user.role.add(chef_role)
            return HttpResponse("You are a chef now.")
        else:
            return HttpResponse("You are already a chef.")
    else:
        return HttpResponse("Something went wrong.")