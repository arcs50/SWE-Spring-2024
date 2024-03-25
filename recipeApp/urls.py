from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("subscriberhome", views.subscriber_home, name="subscriber_home"),
    path("shefhome", views.index, name="index"),
]
