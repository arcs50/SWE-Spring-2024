from django.forms import ModelForm, TextInput, NumberInput, Select
from .models import Recipe, Ingredient, Instruction

class recipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ["chef", "posted_time"]
        # widgets = {
        #     'title': TextInput(attrs={'placeholder': 'Recipe title'}),
        #     'prep_time_minutes':NumberInput(attrs={'placeholder':'prep time in minutes'}),
        #     'cook_time_minutes':NumberInput(attrs={'placeholder':'cook time in minutes'}),
        #     'servings':NumberInput(attrs={'placeholder':'number of servings'})
        # }

class ingredientForm(ModelForm):
    class Meta:
        model = Ingredient
        exclude = ["recipe"]
        