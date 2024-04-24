from django.forms import ModelForm, TextInput, NumberInput, Select
from .models import ChefSubscription

class ChefSubscriptionForm(ModelForm):
    class Meta:
        model = ChefSubscription
        exclude = ["chef"]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["time_quantity"].widget.attrs.update({"class": "form-control"})
            self.fields["time_unit"].widget.attrs.update({"class": "form-control"})
            self.fields["price"].widget.attrs.update({"class": "form-control"})
            self.fields["title"].widget.attrs.update({"class": "form-control"})
