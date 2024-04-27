from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import user_profile_view

from . import views
from .views import SignUpView

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("home/", TemplateView.as_view(template_name="home.html"), name="home"),
    path("userprofile/", views.user_profile_view, name="view_user_profile"),
    path("userprofile/edit/", views.edit_user_profile, name="edit_user_profile"),
    path("change_password/", views.change_password, name="change_password"),
]
