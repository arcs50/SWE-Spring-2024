from django.db import models

# Create your models here.


class Product(models.Model):
    name=models.CharField(max_length=100)
    stripe_product_id= models.CharField(default='pr_12345',max_length=100)
    
    def __str__(self):
        return self.name

class Price(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    stripe_price_id=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
