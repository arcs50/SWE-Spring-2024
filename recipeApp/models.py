import math
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from userAccount.models import Person
from django.db.models import Avg

# Create your models here.
class ChefProfile(models.Model):
    chef = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    display_email = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title, self.description

class SocialMedia(models.Model):
    chef_prof = models.ForeignKey(ChefProfile, on_delete=models.CASCADE)
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
    description = models.TextField()
    posted_time = models.DateField(default=timezone.now)
    pinned = models.BooleanField(default=False)
    free_to_nonsubscriber = models.BooleanField(default=False)
    prep_time_minutes = models.PositiveIntegerField(validators = [MaxValueValidator(9999)])
    cook_time_minutes = models.PositiveIntegerField(validators = [MaxValueValidator(9999)])
    servings = models.PositiveIntegerField(validators = [MaxValueValidator(999)])
    recipe_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ["chef","title"]

    def is_chef(self, user):
        return self.chef == user

    def get_time(self, time):
        hour = int(time / 60)
        min = int(time % 60)
        res = ""
        if hour > 0:
            res += str(hour) + " hr "
        if min > 0:
            res += str(min) + " min"
        return res

    def get_total_time(self):
        time = self.prep_time_minutes + self.cook_time_minutes
        return self.get_time(int(time))
    
    def get_prep_time(self):
        return self.get_time(self.prep_time_minutes)
    
    def get_cook_time(self):
        return self.get_time(self.cook_time_minutes)
    
    def get_avg_rating(self):
        ratings = Rating.objects.filter(recipe_id=self.id)
        avg_rating = ratings.aggregate(Avg("stars", default=0))['stars__avg']
        avg_rating_full = int(avg_rating)
        avg_rating_partial = math.ceil(avg_rating % 1)
        avg_rating_empty = 5 - avg_rating_full - avg_rating_partial
        data = {
            'avg_rating':avg_rating,
            'avg_rating_full':range(avg_rating_full),
            'avg_rating_partial':range(avg_rating_partial),
            'avg_rating_empty':range(avg_rating_empty)
        }
        return data
    
    def get_count_rating(self):
        ratings = Rating.objects.filter(recipe_id=self.id)
        count_rating = ratings.count()
        res = str(count_rating)
        if count_rating > 1 or count_rating < 1:
            res += " people" 
        else:
            res += " person"
        return res
        


class Collection(models.Model):
    chef = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length = 250)
    creation_time = models.DateField(default=timezone.now)
    recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.title
    


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food = models.CharField(max_length=250)
    quantity = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
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
        ("kg","kilogram"),
        ("slice","slice"),
        ("slices","slices")
    }
    measurement = models.CharField(max_length=15, choices=MEASUREMENTS)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.food
    
    def get_quantity(self):
        if self.quantity == 0:
            return ''
        return self.quantity.normalize()

    def get_measurement(self):
        if self.measurement == 'na':
            return ' '
        else:
            return self.measurement

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    posted_time = models.DateField(default=timezone.now)

    def __str__(self):
        return self.text
    def get_commenter(self):
        person = Person.objects.get(email=self.commenter)
        return person.first_name

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
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
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