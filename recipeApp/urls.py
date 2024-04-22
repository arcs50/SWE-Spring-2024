from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from . import views
from .views import CreateUpdateRecipe, ViewRecipe

urlpatterns = [
    path("discover", views.discover, name="discover"),
    path("subscriberhome", views.subscriber_home, name="subscriber_home"),
    path("chefhome", views.index, name="index"),
    path("search", views.index, name="search"),
    path("create_recipe/", CreateUpdateRecipe, name="create_recipe"),
    path("update_recipe/<int:recipe_id>", CreateUpdateRecipe, name="update_recipe"),
    path("view_recipe/<int:recipe_id>", ViewRecipe, name="view_recipe")
<<<<<<< HEAD
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

>>>>>>> 5b71648e5dabe47f02b0c4bded184d7000ebb028
