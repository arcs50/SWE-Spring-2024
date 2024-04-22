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
from flask import redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404, render
from .models import ChefSubscription, SiteSubscription
from django.contrib.auth import get_user_model

stripe.api_key= settings.STRIPE_SECRET_KEY
YOUR_DOMAIN="http://127.0.0.1:8000"


# Create your views here.
def site_subscription(request):
    return HttpResponse("Hello, world. You're at the site subscriptions index.")

def ManageSubscriptionView(request):
    context = {}
    if request.method == 'POST':
        form = ChefSubscriptionForm(request.POST)
        if 'submit' in request.POST:
            if form.is_valid():
                # Assuming that form.instance.chef will be set to request.user in the form's save method
                subscription = form.save(commit=False)
                subscription.chef = request.user
                subscription.active = True
                
                # Now let's create a product in Stripe
                try:
                    # Create a product
                    product = stripe.Product.create(name=subscription.title)
                    # Create a price
                    price = stripe.Price.create(
                        unit_amount=int(subscription.price * 100),  # Price in cents
                        currency="usd",
                        recurring={"interval": subscription.get_interval_display().lower()},  # Convert to stripe format
                        product=product.id,
                    )
                    subscription.stripe_price_id = price.id  # Save the Stripe price ID to your model
                    subscription.save()
                except stripe.error.StripeError as e:
                    # Handle Stripe exceptions
                    context['error'] = str(e)
                    return render(request, 'manage_subscriptions.html', context)

                return redirect('create_chef_subscription')
            else:
                context['form'] = ChefSubscriptionForm()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            chef_sub = ChefSubscription.objects.get(id=pk)
            chef_sub.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            chef_sub = ChefSubscription.objects.get(id=pk)
            form = ChefSubscriptionForm(instance=chef_sub)
    
    else:  # GET request
        form = ChefSubscriptionForm()
    
    chef_subscriptions = ChefSubscription.objects.filter(chef=request.user)
    print(chef_subscriptions)
    context.update({
        'form': form,
        'chef_subscriptions': chef_subscriptions,
    })
    
    return render(request, 'manage_subscriptions.html', context)

        


User = get_user_model()

def subscribeToChef(request, chef_id):
    # chef = get_object_or_404(User, pk=chef_id)
    chef_subscriptions = ChefSubscription.objects.filter(chef_id=request.user.id)
    print(chef_subscriptions[0])
    # If you have a model for chef profile, fetch it here, e.g.,
    # chef_profile = ChefProfile.objects.get(user=chef)

    context = {
        #'chef': chef,
        'chef_subscriptions': chef_subscriptions,
        # 'chef_profile': chef_profile, if you have a separate model for chef profiles
    }
    return render(request, 'view_chef_subscriptions.html', context)


