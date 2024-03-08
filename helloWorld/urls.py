from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("", views.hello, name="hello"),
    path("testdb/", views.testdb, name="testdb"),
    path("helloworld/", views.helloworld, name="helloworld"),
]