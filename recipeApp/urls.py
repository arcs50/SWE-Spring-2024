from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.main_site, name="main_site"),
    path("subscriberhome", views.subscriber_home, name="subscriber_home"),
    path("chefhome", views.index, name="index"),
]
