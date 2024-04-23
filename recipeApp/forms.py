from django.forms import ModelForm, TextInput, NumberInput, Select, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Recipe, Ingredient, Instruction, Rating, Comment, ChefProfile, SocialMedia, Collection
from django.forms.models import inlineformset_factory

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ["chef", "posted_time"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["prep_time_minutes"].widget.attrs.update({"class": "form-control"})
        self.fields["cook_time_minutes"].widget.attrs.update({"class": "form-control"})
        self.fields["servings"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "rows":"3"})
        self.fields["pinned"].widget.attrs.update({"class":"form-check-input", "type":"checkbox", "role":"switch"})
        self.fields["free_to_nonsubscriber"].widget.attrs.update({"class":"form-check-input", "type":"checkbox", "role":"switch"})
        self.fields["recipe_image"].widget.attrs.update({"class": "form-control"})
        # widgets = {
        #     'title': TextInput(attrs={'placeholder': 'Recipe title'}),
        #     'prep_time_minutes':NumberInput(attrs={'placeholder':'prep time in minutes'}),
        #     'cook_time_minutes':NumberInput(attrs={'placeholder':'cook time in minutes'}),
        #     'servings':NumberInput(attrs={'placeholder':'number of servings'})
        # }

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        exclude = ["recipe"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["measurement"].widget.attrs.update({"class": "form-control"})
        self.fields["quantity"].widget.attrs.update({"class":"form-control"})
        self.fields["food"].widget.attrs.update({"class":"form-control"})
        self.fields["order"].widget.attrs.update({"class":"form-control"})


IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm,
    extra=1, can_order=True, can_delete=True, can_delete_extra=True)
        

class InstructionForm(ModelForm):
    class Meta:
        model = Instruction
        exclude = ["recipe"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update({"class": "form-control", "rows":"1"})
        self.fields["order"].widget.attrs.update({"class":"form-control"})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['recipe','commenter','posted_time']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update({"class": "form-control", "rows":"3"})

class ChefProfileForm(ModelForm):
    class Meta:
        model=ChefProfile
        exclude = ['chef']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "rows":"3"})
        self.fields["display_email"].widget.attrs.update({"class":"form-check-input", "type":"checkbox", "role":"switch"})
        self.fields["profile_picture"].widget.attrs.update({"class": "form-control"})

class SocialMediaForm(ModelForm):
    class Meta:
        model = SocialMedia
        exclude = ['chef']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["platform"].widget.attrs.update({"class": "form-control"})
        self.fields["handle"].widget.attrs.update({"class": "form-control"})
        self.fields["url"].widget.attrs.update({"class": "form-control"})


class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'recipes']  # include 'recipes' to manage the M2M relationship
        recipes = ModelMultipleChoiceField(
            queryset = Recipe.objects.all().order_by('title'),
            widget=CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        # Optionally, modify the queryset for 'recipes' if you want to limit choices or order them
        #self.fields['recipes'].queryset = Recipe.objects.filter(chef=user).order_by('title')
        self.fields['recipes'].widget.attrs.update({"class": "form-control"})
        self.fields["title"].widget.attrs.update({"class": "form-control"})


# class CollectionForm(ModelForm):
#     class Meta:
#         model = Collection

#     # Representing the many to many related field in Pizza
#     recipes = ModelMultipleChoiceField(queryset=Recipe.objects.all())

#     # Overriding __init__ here allows us to provide initial
#     # data for 'toppings' field
#     def __init__(self, *args, **kwargs):
#         # Only in case we build the form from an instance
#         # (otherwise, 'toppings' list should be empty)
#         if kwargs.get('instance'):
#             # We get the 'initial' keyword argument or initialize it
#             # as a dict if it didn't exist.                
#             initial = kwargs.setdefault('initial', {})
#             # The widget for a ModelMultipleChoiceField expects
#             # a list of primary key for the selected data.
#             initial['recipes'] = [t.pk for t in kwargs['instance'].recipe_set.all()]

#         ModelForm.__init__(self, *args, **kwargs)

#     # Overriding save allows us to process the value of 'toppings' field    
#     def save(self, commit=True):
#         # Get the unsave Pizza instance
#         instance = ModelForm.save(self, False)

#         # Prepare a 'save_m2m' method for the form,
#         old_save_m2m = self.save_m2m
#         def save_m2m():
#            old_save_m2m()
#            # This is where we actually link the pizza with toppings
#            instance.recipe_set.clear()
#            instance.recipe_set.add(*self.cleaned_data['recipes'])
#         self.save_m2m = save_m2m

#         # Do we need to save all changes now?
#         if commit:
#             instance.save()
#             self.save_m2m()

#         return instance