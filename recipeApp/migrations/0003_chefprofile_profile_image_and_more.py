# Generated by Django 4.2.11 on 2024-04-21 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeApp', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chefprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement',
            field=models.CharField(choices=[('oz', 'ounce'), ('gal', 'gallon'), ('cup', 'cup'), ('tsp', 'teaspoon'), ('fl oz', 'fluid ounce'), ('g', 'gram'), ('tbsp', 'tablespoon'), ('L', 'liter'), ('na', 'none'), ('pt', 'pint'), ('kg', 'kilogram'), ('lb', 'pound'), ('qt', 'quart'), ('ml', 'milliliter')], max_length=15),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='platform',
            field=models.CharField(choices=[('I', 'Instagram'), ('F', 'Facebook'), ('Y', 'YouTube'), ('TW', 'Twitter'), ('TK', 'TikTok'), ('S', 'Snapchat')], max_length=2),
        ),
    ]
