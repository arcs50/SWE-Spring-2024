from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.db import IntegrityError
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.http import JsonResponse
#import pdb

import time
from recipeApp.forms import RecipeForm, IngredientForm, InstructionForm, SocialMediaForm, ChefProfileForm,IngredientFormSet
from recipeApp.models import Recipe, ChefProfile, Ingredient, Instruction, SocialMedia
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

# chef profile page
# def edit_chef_home(request, chef_id):
#     # check login
#     if not request.user.is_authenticated:
#         return redirect(reverse("signup"))
#     # check chef role
#     if not request.user.role.filter(role='C').exists():
#         return HttpResponse("You are not a chef.")
#     # check user id
#     if chef_id != request.user.id:
#         return HttpResponse("You have no access to this page.")
    
#     # chef_id = request.user.id
#     recipes = Recipe.objects.filter(chef_id = request.user.id)
#     # chef_profile = ChefProfile()
    
#     # if already have chef profile:
#     if ChefProfile.objects.filter(chef_id = request.user.id).exists(): 
#         chef_profile = get_object_or_404(ChefProfile, id = chef_id)
#     else:
#         chef_profile = ChefProfile()
    

#     social_media_queryset = SocialMedia.objects.filter(chef_id=chef_id)

#     SocialMediaFormSet = modelformset_factory(SocialMedia, form=SocialMediaForm, extra=1, can_delete=True, can_delete_extra=True)

#     if request.method == 'POST' and 'save_profile' in request.POST: # update
#         form = ChefProfileForm(request.POST, request.FILES, instance = chef_profile)
#         social_media_formset = SocialMediaFormSet(request.POST, queryset=social_media_queryset)
#         if form.is_valid() and social_media_formset.is_valid():
#             try:
#                 with transaction.atomic():
#                     saved_profile = form.save(commit=False)
#                     saved_profile.chef_id = request.user.id
#                     saved_profile.save()
#                     social_media_formset.save()
#                     return redirect('successfully saved')
#                     # return redirect('view_chef_home', recipe_id = saved_profile.id)
#             except Exception as e:  
#                 form.add_error(None, f'An error occurred: {str(e)}')
#                 # return JsonResponse({'success': False, 'error_message': str(e)}, status=400)
#         else: 
#             print(social_media_formset.errors)
#     else: # create a new one
#         form = ChefProfileForm(instance = chef_profile)
#         social_media_formset = SocialMediaFormSet(queryset=social_media_queryset) 

    
#     params = {
#         'chef_id': chef_id,
#         'recipes': recipes,
#         'form': form,
#         'social_media_formset': social_media_formset
#     }
    
#     return render(request, 'edit_chef_home.html', params)


def edit_chef_home(request, chef_id):
    # check login
    if not request.user.is_authenticated:
        return redirect(reverse("signup"))
    # check chef role
    if not request.user.role.filter(role='C').exists():
        return HttpResponse("You are not a chef.")
    # check user id
    if chef_id != request.user.id:
        return HttpResponse("You have no access to this page.")
    
    # chef_id = request.user.id
    recipes = Recipe.objects.filter(chef_id = request.user.id)
    # chef_profile = ChefProfile()
    
    # if already have chef profile:
    # if ChefProfile.objects.filter(chef_id = request.user.id).exists(): 
    #     chef_profile = ChefProfile.objects.filter(chef_id = request.user.id)
    # else:
    #     chef_profile = ChefProfile()
    chef_profile, created = ChefProfile.objects.get_or_create(chef_id=request.user.id)
    
    # if SocialMedia.objects.filter(chef_id = request.user.id).exists(): 
    #     social_media = SocialMedia.objects.filter(chef_id = request.user.id)
    # else:
    #     social_media = SocialMedia()
    social_media, created = SocialMedia.objects.get_or_create(chef_id=request.user.id)

    if request.method == 'POST' and 'save_profile' in request.POST: # update
        form = ChefProfileForm(request.POST, request.FILES, instance = chef_profile)
        social_media_form = SocialMediaForm(request.POST, instance = social_media)
        if form.is_valid() and social_media_form.is_valid():
            try:
                with transaction.atomic():
                    saved_profile = form.save(commit=False)
                    saved_profile.chef_id = request.user.id
                    saved_profile.save()
                    saved_media = social_media_form.save(False)
                    saved_media.chef_id = request.user.id
                    social_media_form.save()
                    messages.success(request, 'Successfully saved')
                    return redirect('edit_chef_home', chef_id=chef_id)
                    # return redirect('view_chef_home', recipe_id = saved_profile.id)
            except Exception as e:  
                form.add_error(None, f'An error occurred: {str(e)}')
                # return JsonResponse({'success': False, 'error_message': str(e)}, status=400)
        else: 
            print(social_media_form.errors)
    else: # create a new one
        form = ChefProfileForm(instance = chef_profile)
        social_media_form = SocialMediaForm(instance = social_media) 

    
    params = {
        'chef_id': chef_id,
        'recipes': recipes,
        'form': form,
        'social_media_form': social_media_form
    }
    
    return render(request, 'edit_chef_home.html', params)

def view_chef_home(request, chef_id):
    # check login
    if not request.user.is_authenticated:
        return redirect(reverse("signup"))
    
    recipes = Recipe.objects.filter(chef_id = request.user.id)
    chef_profile = get_object_or_404(ChefProfile, chef_id = chef_id)
    # social_media = SocialMedia.objects.filter(id = chef_id)
    social_media = get_object_or_404(SocialMedia, chef_id = chef_id)
    params = {
        'chef_id': chef_id,
        'recipes': recipes,
        'chef_profile': chef_profile,
        'social_media': social_media
    }

    return render(request, 'view_chef_home.html', params)

def recipe_sort(request):
    sort_criteria = request.GET.get('sort', 'newest')  # Default to sorting by newest
    if sort_criteria == 'newest':
        recipes = Recipe.objects.order_by('-posted_time')  # Sort by newest
    else:
        recipes = Recipe.objects.order_by('posted_time')   # Sort by oldest

    # Serialize the recipes and return as JSON response
    serialized_recipes = [{'title': recipe.title, 'recipe_image': recipe.recipe_image.url, 'url': recipe.get_absolute_url()} for recipe in recipes]
    return JsonResponse(serialized_recipes, safe=False)

