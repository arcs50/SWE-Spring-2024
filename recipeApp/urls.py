from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from .views import CreateUpdateRecipe, ViewRecipe

urlpatterns = [
    path("discover", views.discover, name="discover"),
    path("subscriberhome", views.subscriber_home, name="subscriber_home"),
    path("edit_chef_home/<int:chef_id>", views.edit_chef_home, name="edit_chef_home"),
    path("view_chef_home/<int:chef_id>", views.view_chef_home, name="view_chef_home"),
    path("search", views.index, name="search"),
    path("create_recipe/", CreateUpdateRecipe, name="create_recipe"),
    path("update_recipe/<int:recipe_id>", CreateUpdateRecipe, name="update_recipe"),
    path("view_recipe/<int:recipe_id>", ViewRecipe, name="view_recipe")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

