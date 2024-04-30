from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

# Create your models here.

class ChefSubscription(models.Model):
    chef = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    TIME_UNITS = {
        ("W","Week"),
        ("M","Month"),
        ("Y","Year")
    }
    time_unit = models.CharField(max_length=1, choices=TIME_UNITS)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    active = models.BooleanField(default=True)
    stripe_price_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ["chef","title","time_quantity","time_unit","price"]

    def __str__(self):
        return self.title
    
    def get_caption(self):
        caption = "$" 
        if self.price % 1 == 0:
            caption += str(int(self.price)) + "/"
        else:
            caption += str(self.price) + "/"
        plural = False
        if self.time_quantity > 1:
            caption += str(self.time_quantity) + " "
            plural = True
        if self.time_unit == 'W':
            caption += "Week"
        elif self.time_unit == "M":
            caption += "Month"
        elif self.time_unit == "Y":
            caption += "Year"
        if plural:
            caption += "s"
        return caption

    def get_time_unit(self):
        if self.time_unit == 'W':
            return "week"
        elif self.time_unit == "M":
            return "month"
        else:
            return "year"

class SubscriptionToChef(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chef_subscription = models.ForeignKey(ChefSubscription, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    blocked = models.BooleanField(default=False)
        
    class Meta:
        unique_together = ["subscriber","chef_subscription","start_date"]

class SiteSubscription(models.Model):
    title = models.CharField(max_length=255)
    time_quantity = models.PositiveIntegerField()
    TIME_UNITS = {
        ("W","Week"),
        ("M","Month"),
        ("Y","Year")
    }
    time_unit = models.CharField(max_length=10, choices=TIME_UNITS)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stripe_price_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title

class SubscriptionToSite(models.Model):
    chef = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site_subscription = models.ForeignKey(SiteSubscription, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
