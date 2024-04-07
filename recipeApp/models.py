from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class ChefProfile(models.Model):
    chef = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    display_email = models.BooleanField(default=False)

    def __str__(self):
        return self.title, self.description

class SocialMedia(models.Model):
    chef = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    PLATFORMS = {
        ("TW","Twitter"),
        ("I","Instagram"),
        ("F","Facebook"),
        ("Y","YouTube"),
        ("TK","TikTok"),
        ("S","Snapchat")
    }
    platform = models.CharField(max_length=2, choices=PLATFORMS)
    handle = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.handle


class Recipe(models.Model):
    chef = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length = 255)
    posted_time = models.DateField(default=timezone.now)
    pinned = models.BooleanField(default=False)
    free_to_nonsubscriber = models.BooleanField(default=False)
    prep_time_minutes = models.PositiveIntegerField(validators = [MaxValueValidator(9999)])
    cook_time_minutes = models.PositiveIntegerField(validators = [MaxValueValidator(9999)])
    servings = models.PositiveIntegerField(validators = [MaxValueValidator(999)])

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ["chef","title"]


class Collection(models.Model):
    title = models.CharField(max_length = 250)
    creation_time = models.DateField(default=timezone.now)
    recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.title

class Food(models.Model):
    food = models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return self.food

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    MEASUREMENTS = {
        ("na","none"),
        ("tsp","teaspoon"),
        ("tbsp","tablespoon"),
        ("cup","cup"),
        ("pt","pint"),
        ("qt","quart"),
        ("gal","gallon"),
        ("oz","ounce"),
        ("fl oz","fluid ounce"),
        ("lb","pound"),
        ("ml","milliliter"),
        ("L","liter"),
        ("g","gram"),
        ("kg","kilogram")
    }
    measurement = models.CharField(max_length=15, choices=MEASUREMENTS)
    ingredient_number = models.IntegerField(validators = [MaxValueValidator(999)])
    
    class Meta:
        unique_together = ["recipe","ingredient_number"]

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    instruction_number = models.PositiveIntegerField(validators = [MaxValueValidator(999)])
    text = models.TextField()

    def __str__(self):
        return self.text

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_parent = models.ForeignKey('self', on_delete=models.CASCADE)
    text = models.TextField()
    posted_time = models.DateField(default=timezone.now)

    def __str__(self):
        return self.text

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.IntegerField(
        default=0, 
        validators=[MaxValueValidator(5),MinValueValidator(0)]
    )
    
    class Meta:
        unique_together = ["recipe","rater"]
        
class GroceryList(models.Model):
    ingredients = models.ManyToManyField(Ingredient)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class BookmarkedRecipes(models.Model):
    recipe = models.ManyToManyField(Recipe)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Address(models.Model):
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, default="Zanesville")
    STATE_CHOICES = [
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("DC", "District of Columbia"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming"),
    ]
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default="OH")
    zip_code = models.CharField(max_length=5, default="43701")

    def __str__(self):
        return self.address_1, self.address_2, self.city, self.state, self.zip_code

class PaymentInfo(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    cardnum = models.BigIntegerField()
    exp_date = models.DateField()
    cvv = models.IntegerField()
    

class Picture(models.Model):
    caption = models.TextField()
    picture_address = models.URLField(max_length=255, unique=True)

class Video(models.Model):
    video_address = models.URLField(max_length=255,unique=True)
    caption = models.TextField()