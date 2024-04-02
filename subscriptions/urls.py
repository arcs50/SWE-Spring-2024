from django.urls import path
from .views import CreateChefSubscriptionView

from . import views

urlpatterns = [
    path("", views.site_subscription, name="site_subscription"),
    path("manage_subscriptions/", CreateChefSubscriptionView.as_view(), name="create_chef_subscription"),
]