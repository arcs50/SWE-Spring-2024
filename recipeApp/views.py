from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

import time
from recipeApp.models import Recipe
from subscriptions.models import SubscriptionToChef


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the recipeApp index.")

def discover(request):
    params = {}   
    if request.user.is_authenticated:
        params['is_authenticated'] = True
        params['avator_dir'] = 'images/sad_cat.jpg'
    
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
        'sub_avator_dir': 'images/sad_cat.jpg',
        'sub_recipes': sub_recipes
    }
    
    params = {}
    
    

    return render(request, 'subhomepage.html', params_sample)