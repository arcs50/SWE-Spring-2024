from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RecipeForm, IngredientForm, InstructionForm, IngredientFormSet
from django.utils import timezone
from .models import Recipe, Ingredient, Instruction
from django.db import IntegrityError
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
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
