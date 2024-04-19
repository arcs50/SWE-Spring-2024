from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone, reverse
from django.db import IntegrityError
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
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
    ingredients = Ingredient.objects.filter(id=recipe_id)
    context= {
        'recipe':recipe,
        'ingredients':ingredients
        }
    return render(request, 'view_recipe.html', context)



# #@login_required
# def CreateRecipe(request, recipe_id='None'):
#     recipes = Recipe.objects.filter(recipe_id=request.user.id)
#     ingredientFormSet = modelformset_factory(Ingredient, form=ingredientForm, extra = 2, can_delete=True, can_order=True, max_num=60) 
#     if request.method == 'POST' and 'save_recipe' in request.POST:
#             form = recipeForm(request.POST)
#             ingredient_formset = ingredientFormSet(request.POST)
#             if form.is_valid() and ingredient_formset.is_valid():  
#                 try:
#                     with transaction.atomic():
#                         recipe = form.save(commit=False)
#                         recipe.chef_id = request.user.id
#                         recipe.save()
#                         #ingredients = ingredient_formset.save(commit=False)
#                         for ingredient in ingredient_formset:
#                             ingredient.save(commit=False)
#                             ingredient.recipe = recipe
#                             ingredient.save()
#                         #ingredient_formset.save()
#                     # form = recipeForm
#                     # ingredient_formset = ingredientFormSet  
#                 except Exception as e:  # To catch and log any error
#                     form.add_error(None, f'An error occurred: {str(e)}')
#             else:
#                  print(ingredient_formset.errors) 
#     else:
#          form = recipeForm()
#          ingredient_formset = ingredientFormSet(queryset=Ingredient.objects.none()) 
#     context = {
#         'chef_id': chef_id,
#         'recipes': recipes,
#         'form': form,
#         'formset': ingredient_formset
#     }   
#     return render(request, 'create_recipe.html', context)

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
