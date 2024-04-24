from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import ChefSubscriptionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ChefSubscription
from recipeApp.models import ChefProfile
import stripe
import os
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404, render, redirect
from .models import ChefSubscription, SiteSubscription, SubscriptionToChef
from django.contrib.auth import get_user_model

stripe.api_key= settings.STRIPE_SECRET_KEY
YOUR_DOMAIN="http://127.0.0.1:8000"


# Create your views here.
def site_subscription(request):
    return HttpResponse("Hello, world. You're at the site subscriptions index.")

import stripe

def CreateUpdateChefSubscription(request, chef_id, chef_subscription_id=None):
    if request.user.is_authenticated and request.user.id == chef_id:
        context = {}
        chef_subscription = None

        # Check if we are updating an existing subscription
        if chef_subscription_id:
            chef_subscription = get_object_or_404(ChefSubscription, id=chef_subscription_id)
        
        form = ChefSubscriptionForm(request.POST or None, instance=chef_subscription)

        if request.method == 'POST':
            if form.is_valid():
                subscription = form.save(commit=False)
                subscription.chef = request.user
                subscription.active = True
                
                try:
                    if chef_subscription_id and subscription.stripe_price_id:
                        # Update existing Stripe price
                        price = stripe.Price.modify(
                            subscription.stripe_price_id,
                            unit_amount=int(subscription.price * 100)  # Update price in cents
                        )
                        # Update existing Stripe product (if necessary)
                        stripe.Product.modify(
                            subscription.stripe_product_id,
                            name=subscription.title
                        )
                    else:
                        # Create new Stripe product
                        product = stripe.Product.create(name=subscription.title)
                        # Create new Stripe price
                        price = stripe.Price.create(
                            unit_amount=int(subscription.price * 100),  # Price in cents
                            currency="usd",
                            recurring={"interval": subscription.get_time_unit(), "interval_count": subscription.time_quantity},
                            product=product.id
                        )
                        subscription.stripe_product_id = product.id
                        subscription.stripe_price_id = price.id  # Save the Stripe price ID

                    subscription.save()
                    return redirect('view_chef_subscription', chef_id=chef_id)

                except stripe.error.StripeError as e:
                    # Handle Stripe exceptions
                    context['error'] = str(e)

        context.update({
            'form': form,
            'chef_id': chef_id, 
            'chef_subscription_id': chef_subscription_id
        })

        return render(request, 'manage_subscriptions.html', context)

    else:
        return redirect('signup')

        


User = get_user_model()

def ViewChefSubscriptions(request, chef_id):
    chef_subscriptions = ChefSubscription.objects.filter(chef_id=chef_id)
    is_chef=False
    if request.user.is_authenticated:
        if chef_id == request.user.id:
            is_chef = True
    
    if request.method == 'POST':
           pk = request.POST.get('delete')
           chef_sub = ChefSubscription.objects.get(id=pk)
           subs_to_chef=SubscriptionToChef.objects.filter(chef_subscription=chef_sub)
           if subs_to_chef.count()>0:
               chef_sub.active=False
               chef_sub.save()
           else:    
                chef_sub.delete()
    context = {
        'chef_subscriptions': chef_subscriptions,
        'is_chef':is_chef,
        'chef_id':chef_id
    }
    return render(request, 'view_chef_subscriptions.html', context)



def payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return HttpResponse("No session ID found.", status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        user_id = session.metadata['user_id']  # Assuming you stored user_id in metadata
        stripe_price_id = session.metadata['stripePriceId']

        # Find or create the ChefSubscription (assuming you have a way to relate a Stripe price ID to a ChefSubscription)
        chef_subscription = ChefSubscription.objects.get(stripe_price_id=stripe_price_id)

        # Record the subscription to the chef
        subscription = SubscriptionToChef.objects.create(
            subscriber_id=user_id,
            chef_subscription=chef_subscription
        )
        return redirect('view_chef_prof', chef_id=chef_subscription.chef.id)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


def create_checkout_session(request):
    if request.method == 'POST':
        try:
            # Access the form data using Django's request.POST dictionary
            print(request.POST.get('stripePriceId'))
            stripe_price_id = request.POST.get('stripePriceId') # Assuming you need this for Stripe
            success_url = request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}'
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': stripe_price_id,  # Use the correct Stripe Price ID from the form
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=success_url.replace('{CHECKOUT_SESSION_ID}', '{CHECKOUT_SESSION_ID}'), # Correctly format the URL
                cancel_url=request.build_absolute_uri('/cancel.html'),
                metadata={'user_id': request.user.id,'stripePriceId':stripe_price_id}
            )
            return HttpResponseRedirect(checkout_session.url)
        except Exception as e:
            return HttpResponse(str(e))  # Display errors

    # If it's not a POST request, or if anything goes wrong, show the form again
    chef_subscriptions = ChefSubscription.objects.filter(chef_id=request.user.id)
    context = {
        'chef_subscriptions': chef_subscriptions,
    }
    return render(request, 'view_chef_subscriptions.html',context)