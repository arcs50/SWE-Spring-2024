import math
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
<<<<<<< HEAD
from .forms import RecipeForm, IngredientForm, InstructionForm, IngredientFormSet, CommentForm
from .models import Recipe, Ingredient, Instruction, BookmarkedRecipes, Rating, Comment
from django.utils import timezone
from django.urls import reverse
>>>>>>> 5b71648e5dabe47f02b0c4bded184d7000ebb028
from django.db import IntegrityError
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.db.models import Avg
#import pdb

import time
from recipeApp.forms import RecipeForm, IngredientForm, InstructionForm, IngredientFormSet
from recipeApp.models import Recipe, ChefProfile, Ingredient, Instruction
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

@login_required
def CreateUpdateRecipe(request, recipe_id=None):
    recipes = Recipe.objects.filter(chef_id=request.user.id)
    recipe = Recipe()
    if recipe_id:
        recipe = get_object_or_404(Recipe, id=recipe_id)
    IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm, extra=1, can_delete=True, can_delete_extra=True)
    InstructionFormSet = inlineformset_factory(Recipe, Instruction, form=InstructionForm, extra=1, can_delete=True, can_delete_extra=True)
    if request.method == 'POST' and 'save_recipe' in request.POST:
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
        instruction_formset = InstructionFormSet(request.POST, instance=recipe)
        if form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():  
            try:
                with transaction.atomic():
                    saved_recipe = form.save(commit=False)
                    saved_recipe.chef_id = request.user.id
                    saved_recipe.save()
                    ingredient_formset.save()
                    instruction_formset.save()
                    return redirect('view_recipe', recipe_id=saved_recipe.id)
            except Exception as e:  # To catch and log any error
                form.add_error(None, f'An error occurred: {str(e)}')
        else:
                print(ingredient_formset.errors) 
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe) 
        instruction_formset = InstructionFormSet(instance=recipe)
         
    context = {
        'recipe_id': recipe_id,
        'recipes': recipes,
        'form': form,
        'formset': ingredient_formset,
        'instruction_formset': instruction_formset
    }   
    return render(request, 'create_update_recipe.html', context)

def ViewRecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = Ingredient.objects.filter(recipe_id=recipe_id)
    instructions = Instruction.objects.filter(recipe_id=recipe_id)
    form = CommentForm()
    try:
        rating = Rating.objects.get(recipe_id=recipe_id, rater=request.user)
        rating = rating.stars
    except Rating.DoesNotExist:
        rating = 0  
    bookmarked = False
    if BookmarkedRecipes.objects.filter(subscriber=request.user, recipe=recipe).count() > 0:
        bookmarked = True    
    if request.method == 'POST':
        if 'bookmark' in request.POST:
            if not bookmarked:
                bookmark = BookmarkedRecipes()
                bookmark.subscriber=request.user
                bookmark.recipe=recipe
                bookmark.save()
                bookmarked = True
            else:
                bookmark = BookmarkedRecipes.objects.get(subscriber=request.user, recipe=recipe)
                bookmark.delete()
                bookmarked = False
        elif 'star_rated' in request.POST or 'star_unrated' in request.POST:
            if 'star_unrated' in request.POST:
                rating += int(request.POST.get('star_unrated')) + 1
            elif 'star_rated' in request.POST:
                rating = int(request.POST.get('star_rated')) + 1
            instance, created = Rating.objects.get_or_create(recipe_id=recipe_id, rater=request.user)
            instance.stars = rating
            instance.save()
        elif 'post' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.recipe = recipe
                form.commenter = request.user
                form.save()
                form = CommentForm()
    ratings = Rating.objects.filter(recipe_id=recipe_id)
    count_rating = ratings.count()
    avg_rating = ratings.aggregate(Avg("stars", default=0))['stars__avg']
    avg_rating_full = int(avg_rating)
    avg_rating_partial = math.ceil(avg_rating % 1)
    avg_rating_empty = 5 - avg_rating_full - avg_rating_partial
    comments = Comment.objects.filter(recipe_id=recipe_id)
    context= {
        'recipe':recipe,
        'ingredients':ingredients,
        'instructions':instructions,
        'bookmarked':bookmarked,
        'count_rating': count_rating,
        'avg_rating':avg_rating, 
        'avg_rating_full': range(avg_rating_full),
        'avg_rating_partial':range(avg_rating_partial),
        'avg_rating_empty':range(avg_rating_empty),
        'rating':range(rating),
        'unrated':range(5-rating),
        'form':form,
        'comments':comments
        }
    return render(request, 'view_recipe.html', context)

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
    sub_recipes = []
    for sub_chef in sub_chefs:
        chef_recipes = Recipe.objects.filter(chef_id=sub_chef.chef_id)
        for chef_recipe in chef_recipes:
            recipe_info = {
                'recipe_id': chef_recipe.id,
                'title': chef_recipe.title,
                'posted_time': chef_recipe.posted_time,
                'chef_name': sub_chef.chef_name,
                'first_img_dir': 'images/sad_cat.jpg'
            }
            sub_recipes.append(recipe_info)
    # sort sub_recipes based on post time
    sub_recipes.sort(key=lambda x:x.posted_time)
    
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
        'sub_chefs': sub_chefs,
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
