from django.contrib import admin
from django.urls import include, path

from . import views
from .views import CreateRecipe

urlpatterns = [
    path("subscriberhome", views.subscriber_home, name="subscriber_home"),
    path("chefhome", views.index, name="index"),
    path("create_recipe/<int:chef_id>", CreateRecipe, name="create_recipe"),
]
