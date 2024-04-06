import stripe
import os
from flask import redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView

stripe.api_key= settings.STRIPE_SECRET_KEY
YOUR_DOMAIN="http://127.0.0.1:8000"

class ProductLandingPageView(TemplateView):
    template_name="landing.html"

    def get_context_data(self, **kwargs: any):
        context=super(ProductLandingPageView,self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context
    
class CreateCheckoutSessionView(View):
    def post(self, request, *args, ** kwargs):
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1P1aLg03nG7roY1gYXubQV0e',
                    'quantity':1
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return HttpResponseRedirect(checkout_session.url)