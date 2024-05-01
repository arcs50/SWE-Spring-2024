from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from userAccount.admin import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Person
from django.contrib import messages
from subscriptions.models import SubscriptionToChef, SubscriptionToSite

# Create your views here.
from django.http import HttpResponse
#from userAccount.models import Role


def index(request):
    return HttpResponse("Hello, world. You're at the recipeApp index.")


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def user_profile_view(request):
    user = request.user
    is_chef = SubscriptionToSite.objects.filter(chef = request.user).exists()
    is_subscriber = SubscriptionToChef.objects.filter(subscriber_id=request.user.id).exists()
    is_admin = request.user.is_admin
    return render(request, 'profile/user_profile.html',
                  {'user': user, 'is_chef': is_chef,
                      'is_subscriber': is_subscriber,
                      'is_admin': is_admin}
                  )


@login_required
def edit_user_profile(request):
    user = request.user
    if request.POST:
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Your profile was successfully updated.')
        return redirect('view_user_profile')
    return render(request, 'profile/edit_user_profile.html', {'user': user})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('view_user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/change_password.html', {'form': form})
