from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import ChefSubscriptionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ChefSubscription
from recipeApp.models import ChefProfile

# Create your views here.
def site_subscription(request):
    return HttpResponse("Hello, world. You're at the site subscriptions index.")


def ManageSubscriptionView(request):
    context={}
    form = ChefSubscriptionForm
    chef_subscriptions = ChefSubscription.objects.filter(chef_id=request.user.id)
    context['chef_subscriptions'] = chef_subscriptions
    if request.method == 'POST':
        if 'submit' in request.POST:
            pk = request.POST.get('submit')
            if not pk: 
                form = ChefSubscriptionForm(request.POST)
                form.instance.chef_id = request.user.id
                form.instance.active = True
            else:
                chef_sub = ChefSubscription.objects.get(id=pk)
                form = ChefSubscriptionForm(request.POST, instance=chef_sub)
            #if form.is_valid():
            form.save()
            form = ChefSubscriptionForm
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            chef_sub = ChefSubscription.objects.get(id=pk)
            chef_sub.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            chef_sub = ChefSubscription.objects.get(id=pk)
            form = ChefSubscriptionForm(instance=chef_sub)

    context['form'] = form
    return render(request, 'manage_subscriptions.html', context)
        

def subscribeToChef(request, chef_id):
    context = {}
    #chef_title = ChefProfile.objects.get(chef_id = chef_id).title
    #context['title'] = chef_title
    chef_subscriptions = ChefSubscription.objects.filter(chef_id=chef_id, active = True)
    context['chef_subscriptions'] = chef_subscriptions
    return render(request, 'view_chef_subscriptions.html', context)

