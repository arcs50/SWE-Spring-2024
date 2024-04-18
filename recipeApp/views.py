from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

import time
from recipeApp.models import Recipe
from userAccount.models import Role
from subscriptions.models import SubscriptionToChef


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
    params_sample = {
        'sub_id': request.user.id,
        'sub_username': request.user.get_username(),
        'sub_avatar_dir': 'images/sad_cat.jpg',
        'sub_recipes': sub_recipes
    }
    
    params = {}

    return render(request, 'subhomepage.html', params_sample)

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