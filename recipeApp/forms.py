from django.forms import ModelForm, TextInput, NumberInput, Select
from .models import Recipe, Ingredient, Instruction, Rating, Comment, ChefProfile, SocialMedia
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