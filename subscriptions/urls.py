from django.urls import path
from .views import CreateUpdateChefSubscription, ViewChefSubscriptions, create_checkout_session, payment_success, view_site_subscriptions, payment_success_site, cancel_view

from . import views

urlpatterns = [
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path("", views.site_subscription, name="site_subscription"),
    path("view_chef_subscription/<int:chef_id>", ViewChefSubscriptions, name="view_chef_subscription"),
    path("create_chef_subscription/<int:chef_id>", CreateUpdateChefSubscription, name="create_chef_subscription"),
    path("update_chef_subscription/<int:chef_id>/<int:chef_subscription_id>", CreateUpdateChefSubscription, name="update_chef_subscription"),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('subscription_cancel',cancel_view, name='subscription_cancel'),
    path('view_site_subscriptions/',view_site_subscriptions, name='view_site_subscriptions'),
    path('payment_success_site/', payment_success_site, name='payment_success_site' )
]