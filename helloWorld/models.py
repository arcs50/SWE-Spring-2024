from django.db import models

# Create your models here.

# table name = appname_classname
class HelloTestModels(models.Model):
    # column define
    name = models.CharField(max_length=20)