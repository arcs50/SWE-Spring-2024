from django.urls import path
from .views import ManageSubscriptionView, subscribeToChef

from . import views

urlpatterns = [
    path("", views.site_subscription, name="site_subscription"),
    path("manage_subscriptions/", ManageSubscriptionView, name="create_chef_subscription"),
    path("view_chef_subscriptions/<int:chef_id>", subscribeToChef, name="view_chef_subscription")
]