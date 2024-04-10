from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views
from .views import SignUpView

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("home/", TemplateView.as_view(template_name="home.html"), name="home"), 
    path("tochefrole/", views.to_chef_role, name="to_chef_role"),
    path("tosubscriberrole/", views.index, name="index"),
]