from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from . import views
from .views import CreateUpdateRecipe, ViewRecipe

urlpatterns = [
    path("subscriberhome", views.subscriber_home, name="subscriber_home"),
    path("chefhome", views.index, name="index"),
    path("create_recipe/", CreateUpdateRecipe, name="create_recipe"),
    path("update_recipe/<int:recipe_id>", CreateUpdateRecipe, name="update_recipe"),
    path("view_recipe/<int:recipe_id>", ViewRecipe, name="view_recipe")
] 

#urlpatterns += staticfiles_urlpatterns()