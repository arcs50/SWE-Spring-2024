from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import CreateChefSubscriptionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ChefSubscription

# Create your views here.
def site_subscription(request):
    return HttpResponse("Hello, world. You're at the site subscriptions index.")

class CreateChefSubscriptionView(LoginRequiredMixin, CreateView):
    form_class = CreateChefSubscriptionForm
    template_name = 'manage_subscriptions.html'
    success_url = reverse_lazy('manage_subscriptions')

    def form_valid(self, form):
        # Set the chef_id field to the logged-in user's ID
        title = ""
        time_qt = form.instance.time_quantity
        time_unit = form.instance.time_unit
        form.instance.chef_id = self.request.user.id
        if time_qt == 1:
            if time_unit == "W":
                title = "Weekly"
            elif time_unit == "M":
                title = "Monthly"
            elif time_unit == "Y":
                title = "Annual"
        elif time_qt == 2:
            if time_unit == "W":
                title = "Bieekly"
            elif time_unit == "M":
                title = "Bimonthly"
            elif time_unit == "Y":
                title = "Biennial"
        else:
            title = time_qt + " " + time_unit
        form.instance.title = title + " Subscription"
            
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the same page
        return self.request.path
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch subscriptions associated with the logged-in user
        chef_subscriptions = ChefSubscription.objects.filter(chef_id=self.request.user.id)
        context['chef_subscriptions'] = chef_subscriptions
        return context