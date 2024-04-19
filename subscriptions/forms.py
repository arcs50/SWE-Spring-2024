from django.forms import ModelForm, TextInput, NumberInput, Select
from .models import ChefSubscription

class ChefSubscriptionForm(ModelForm):
    class Meta:
        model = ChefSubscription
        exclude = ["chef"]
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Subscription title'}),
            'time_quantity': NumberInput(attrs ={'placeholder': 'Time qt.', 'style': 'width:75px'}),
            'time_unit': Select(attrs={'placeholder': 'Time unit','style': 'width:75px'}),
            'price': NumberInput(attrs={'placeholder': 'Price: $','style': 'width:75px'}),
        }