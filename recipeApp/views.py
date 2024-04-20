import math
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RecipeForm, IngredientForm, InstructionForm, IngredientFormSet, CommentForm
from django.utils import timezone
from .models import Recipe, Ingredient, Instruction, BookmarkedRecipes, Rating, Comment
from django.db import IntegrityError
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.db.models import Avg
#import pdb
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the recipeApp index.")

def subscriber_home(request):
    params = {}
    return render(request, 'subhomepage.html', params)

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
