from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from userAccount.admin import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Person

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
            role='C',
            defaults={'id': request.user.id, 'role': 'C'}
        )
        return HttpResponse("You are a chef now.")
    else:
        return HttpResponse("something wrong")


@login_required
def user_profile_view(request):
    user = request.user
    return render(request, 'profile/user_profile.html', {'user': user})
