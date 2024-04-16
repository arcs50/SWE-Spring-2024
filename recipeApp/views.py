from django.shortcuts import render
from django.http import HttpResponse
from .forms import recipeForm, ingredientForm
from django.utils import timezone
from .models import Recipe, Ingredient
from django.db import IntegrityError
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
#import pdb
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the recipeApp index.")

def subscriber_home(request):
    params = {}
    return render(request, 'subhomepage.html', params)

#@login_required
def CreateRecipe(request, chef_id):
    # if settings.DEBUG:
    #     if 'pdb' in request.GET and request.GET['pdb'] == '1':
    #         pdb.set_trace()

    recipes = Recipe.objects.filter(chef_id=request.user.id)
    ingredientFormSet = modelformset_factory(Ingredient, form=ingredientForm, extra = 3, can_delete=True, can_order=True, max_num=60)
    form = recipeForm
    ingredient_formset = ingredientFormSet  
    context = {
        'chef_id': chef_id,
        'recipes': recipes,
        'form': form,
        'formset': ingredient_formset
    }
    if request.method == 'POST' and 'save_recipe' in request.POST:
            form = recipeForm(request.POST)
            ingredient_formset = ingredientFormSet(request.POST)  
            try:
                with transaction.atomic():
                    recipe = form.save(commit=False)
                    recipe.chef_id = request.user.id
                    ingredients = ingredient_formset.save(commit=False)
                    for ingredient in ingredients:
                        ingredient.recipe = recipe
                    if form.is_valid() and ingredient_formset.is_valid():
                        recipe.save()
                        ingredient_formset.save()
                form = recipeForm
                ingredient_formset = ingredientFormSet  
            except Exception as e:  # To catch and log any error
                form.add_error(None, f'An error occurred: {str(e)}')
  
    return render(request, 'create_recipe.html', context)




# if request.method == 'POST':
#         if 'submit' in request.POST:
#             pk = request.POST.get('submit')
#             if not pk: 
#                 form = ChefSubscriptionForm(request.POST)
#                 form.instance.chef_id = request.user.id
#                 form.instance.active = True
#             else:
#                 chef_sub = ChefSubscription.objects.get(id=pk)
#                 form = ChefSubscriptionForm(request.POST, instance=chef_sub)
#             #if form.is_valid():
#             form.save()
#             form = ChefSubscriptionForm
#         elif 'delete' in request.POST:
#             pk = request.POST.get('delete')
#             chef_sub = ChefSubscription.objects.get(id=pk)
#             chef_sub.delete()
#         elif 'edit' in request.POST:
#             pk = request.POST.get('edit')
#             chef_sub = ChefSubscription.objects.get(id=pk)
#             form = ChefSubscriptionForm(instance=chef_sub)
#     context['form'] = form