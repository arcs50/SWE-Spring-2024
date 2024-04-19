from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

import time
from recipeApp.models import Recipe, ChefProfile
from userAccount.models import Role, Person
from subscriptions.models import SubscriptionToChef, ChefSubscription


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the recipeApp index.")

def discover(request):
    params = {}   
    if request.user.is_authenticated:
        params['is_authenticated'] = True
        params['avatar_dir'] = 'images/sad_cat.jpg'
    
    rec_recipes = [
        {
            'recipe_id': '123456',
            'title': 'whwawhawh',
            'posted_time': time.time(),
            'chef_name': 'whawhawa',
            'first_img_dir': 'images/sad_cat.jpg'
        },
        {
            'recipe_id': '654321',
            'title': 'whwawhawh',
            'posted_time': time.time(),
            'chef_name': 'whawhawa',
            'first_img_dir': 'images/sad_cat.jpg'
        }
    ]
    
    rec_chefs = [
        {
            'chef_id': '123456',
            'title': 'whwawhawh',
            'chef_name': 'whawhawa',
            'avatar_dir': 'images/sad_cat.jpg'
        },
        {
            'chef_id': '123456',
            'title': 'whwawhawh',
            'chef_name': 'whawhawa',
            'avatar_dir': 'images/sad_cat.jpg'
        },
    ]
    
    params['rec_recipes'] = rec_recipes
    params['rec_chefs'] = rec_chefs
    
    return render(request, 'discover.html', params)

def subscriber_home(request):
    if not request.user.is_authenticated:
        return redirect(reverse("signup"))
    
    # get user profile
    person = Person.objects.get(id=request.user.id)
    # get subscription
    subscriptions = SubscriptionToChef.objects.filter(subscriber_id=request.user.id)
    valid_subscriptions = []
    for subscription in subscriptions:
        if not subscription.blocked:
            valid_subscriptions.append(subscription)
    # get subscribed chefs info
    sub_chefs = []
    for subscription in valid_subscriptions:
        chef_subscription = ChefSubscription.objects.get(id=subscription.chef_subscription_id)
        chef_profile = ChefProfile.objects.get(chef_id=chef_subscription.chef_id)
        chef_person = Person.objects.get(id=chef_subscription.chef_id)
        sub_chef = {
            'chef_id': chef_profile.chef_id,
            'title': chef_profile.title,
            'chef_name': chef_person.first_name + ' ' + chef_person.last_name,
            'avatar_dir': 'images/sad_cat.jpg'
        }
    # get subscribed recipes
    
    
    # sample params
    sub_recipes = [
        {
            'recipe_id': '123456',
            'title': 'whwawhawh',
            'posted_time': time.time(),
            'chef_name': 'whawhawa',
            'first_img_dir': 'images/sad_cat.jpg'
        },
        {
            'recipe_id': '654321',
            'title': 'whwawhawh',
            'posted_time': time.time(),
            'chef_name': 'whawhawa',
            'first_img_dir': 'images/sad_cat.jpg'
        }
    ]
    params = {
        'sub_id': request.user.id,
        'sub_username': request.user.get_username(),
        'sub_name' : person.first_name + ' ' + person.last_name,
        'sub_avatar_dir': 'images/sad_cat.jpg',
        'sub_recipes': sub_recipes
    }
    

    return render(request, 'subhomepage.html', params)

def chef_home(request):
    if not request.user.is_authenticated:
        return redirect(reverse("signup"))
    role = Role.objects.filter(id=request.user.id)
    if (not role) or (role[0].role != 'C'):
        return HttpResponse("You are not a chef.")
    
    params = {
        'chef_id': request.user.id,
        'chef_username': request.user.get_username(),
        'chef_avatar_dir': 'images/sad_cat.jpg',
        'chef_name': 'aaa',
        'chef_description': 'this is aaa chef.',
        'chef_display_email': 'xxx@gmail.com'
    }
    
    return render(request, 'chefhome.html', params)