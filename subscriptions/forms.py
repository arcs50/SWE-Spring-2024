from django.forms import ModelForm
from .models import ChefSubscription

class CreateChefSubscriptionForm(ModelForm):
    class Meta:
        model = ChefSubscription
        exclude = ["chef", "title"]