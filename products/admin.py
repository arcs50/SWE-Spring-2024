from django.contrib import admin

# Register your models here.
from .models import (Product, Price)
admin.site.register(Product)
admin.site.register(Price)