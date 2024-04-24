import math
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RecipeForm, IngredientForm, InstructionForm, IngredientFormSet, CommentForm, SocialMediaForm, ChefProfileForm, CollectionForm
from .models import Recipe, Ingredient, Instruction, BookmarkedRecipes, Rating, Comment, SocialMedia, Collection
from django.utils import timezone
from django.urls import reverse
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
        
    # get recipes
    recipes = Recipe.objects.all()[:9]
    rec_recipes = []
    for recipe in recipes:
        chef_person = Person.objects.get(id=recipe.chef_id)
        rec_recipe = {
            'recipe_id': recipe.id,
            'chef_name': chef_person.first_name + ' ' + chef_person.last_name,
            'recipe': recipe
        }
        rec_recipes.append(rec_recipe)
    
    # get chefs
    chefs = ChefProfile.objects.all()[:9]
    rec_chefs = []
    for chef in chefs:
        chef_person = Person.objects.get(id=chef.chef_id)
        rec_chef = {
            'chef_id': chef.chef_id,
            'title': chef.title,
            'chef_name': chef_person.first_name + ' ' + chef_person.last_name,
            'avatar_dir': 'images/sad_cat.jpg'
        },
    
    
    params['rec_recipes'] = rec_recipes
    params['rec_chefs'] = rec_chefs
    
    return render(request, 'discover.html', params)

def search(request):
    if not request.POST:
        return redirect(reverse("discover"))
    
    searchtext = request.POST['searchtext']
    
    params = {}   
    if request.user.is_authenticated:
        params['is_authenticated'] = True
        params['avatar_dir'] = 'images/sad_cat.jpg'
        
    # get recipes
    recipes = Recipe.objects.filter(title__icontains=searchtext)
    rec_recipes = []
        
    for recipe in recipes:
        chef_person = Person.objects.get(id=recipe.chef_id)
        rec_recipe = {
            'recipe_id': recipe.id,
            'chef_name': chef_person.first_name + ' ' + chef_person.last_name,
            'recipe': recipe
        }
        rec_recipes.append(rec_recipe)
    
    # get chefs
    chefs = ChefProfile.objects.filter(title__icontains=searchtext)
    rec_chefs = []
    for chef in chefs:
        chef_person = Person.objects.get(id=chef.chef_id)
        rec_chef = {
            'chef_id': chef.chef_id,
            'title': chef.title,
            'chef_name': chef_person.first_name + ' ' + chef_person.last_name,
            'avatar_dir': 'images/sad_cat.jpg'
        }
        rec_chefs.append(rec_chef)
    
    params['rec_recipes'] = rec_recipes
    params['rec_chefs'] = rec_chefs
    
    return render(request, 'search.html', params)

@login_required
def CreateUpdateChefProfile(request, chef_prof_id=None):
    chef_prof = ChefProfile()
    if chef_prof_id:
        chef_prof = get_object_or_404(ChefProfile, id=chef_prof_id)
        #if chef_prof.chef != request.user:
    SocialMediaFormSet = inlineformset_factory(ChefProfile, SocialMedia, form=SocialMediaForm, extra=1, can_delete=True, can_delete_extra=True)
    if request.method =='POST' and 'save_chef_prof' in request.POST:
        form = ChefProfileForm(request.POST, request.FILES, instance=chef_prof)
        socialmedia_formset = SocialMediaFormSet(request.POST, instance=chef_prof)
        if form.is_valid() and socialmedia_formset.is_valid():
            try:
                with transaction.atomic():
                    saved_chef_prof = form.save(commit=False)
                    saved_chef_prof.chef_id = request.user.id
                    saved_chef_prof.save()
                    socialmedia_formset.save()
                    return redirect('view_chef_prof',chef_prof_id = saved_chef_prof.id)
            except Exception as e:  # To catch and log any error
                form.add_error(None, f'An error occurred: {str(e)}')
    else:
        form = ChefProfileForm(instance=chef_prof)
        socialmedia_formset = SocialMediaFormSet(instance=chef_prof) 
         
    context = {
        'chef_prof_id': chef_prof_id,
        'form': form,
        'formset': socialmedia_formset,
    }   
    return render(request, 'create_update_chef_prof.html', context)

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
    is_chef = False
    if request.user.is_authenticated:
        if recipe.chef == request.user:
            is_chef = True
    ingredients = Ingredient.objects.filter(recipe_id=recipe_id)
    instructions = Instruction.objects.filter(recipe_id=recipe_id)
    form = CommentForm()
    bookmarked = False
    rating = 0
    if request.user.is_authenticated:
        try:
            rating = Rating.objects.get(recipe_id=recipe_id, rater=request.user)
            rating = rating.stars
        except Rating.DoesNotExist:
            rating = 0  
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
        'comments':comments,
        'is_chef':is_chef
        }
    return render(request, 'view_recipe.html', context)

def ViewChefProfile(request, chef_prof_id):
    chef_prof = get_object_or_404(ChefProfile, id=chef_prof_id)
    is_chef = False
    if request.user.is_authenticated:
        if chef_prof.chef == request.user:
            is_chef = True
    social_media = SocialMedia.objects.filter(chef_prof_id=chef_prof_id)
    recipes = Recipe.objects.filter(chef=chef_prof.chef)
    collections = Collection.objects.filter(chef=chef_prof.chef)
    context = {
        'chef_prof':chef_prof,
        'is_chef':is_chef,
        'social_media':social_media,
        'recipes':recipes,
        'collections':collections,
        'chef_id':chef_prof.chef.id,
    }
    return render(request, 'view_chef_prof.html', context)

def CreateUpdateCollection(request, chef_id, collection_id=None):
    if request.user.is_authenticated and request.user.id == chef_id:
        collection = Collection()
        if collection_id:
            collection = get_object_or_404(Collection, id=collection_id)
        form = CollectionForm(instance=collection)
        form.fields["recipes"].queryset = Recipe.objects.filter(chef=request.user)
        if request.method == 'POST':
            form = CollectionForm(request.POST, instance=collection)
            if form.is_valid():
                collection = form.save(commit=False)
                collection.chef = request.user
                collection.save()
                form.save_m2m()
                return redirect('view_collection', chef_id=chef_id, collection_id=collection.id)  # Redirect to a success page or the collection detail view
        return render(request, 'create_update_collection.html', {'form': form, 'chef_id': chef_id, 'collection_id':collection_id})



def ViewCollection(request, chef_id, collection_id):
    is_chef = False
    if request.user.is_authenticated:
        if chef_id == request.user.id:
            is_chef = True
    collection = get_object_or_404(Collection, id=collection_id)
    context = {
        'collection':collection,
        'chef_id':chef_id,
        'collection_id':collection_id,
        'user':request.user,
        'is_chef':is_chef
    }
    return render(request, 'view_collection.html', context)



def ViewBookmarks(request, subscriber_id):
    if request.user.is_authenticated and request.user.id == subscriber_id:
        bookmarks = BookmarkedRecipes.objects.filter(subscriber=request.user)
        context = {
            'subscriber_id':subscriber_id,
            'bookmarks':bookmarks
        }
        return render(request, 'view_bookmarks.html', context)
    else:
        return redirect('discover')

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
