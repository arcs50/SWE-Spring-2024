# Generated by Django 4.2.11 on 2024-04-23 00:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipeApp', '0014_alter_ingredient_measurement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='chef',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement',
            field=models.CharField(choices=[('L', 'liter'), ('fl oz', 'fluid ounce'), ('oz', 'ounce'), ('qt', 'quart'), ('lb', 'pound'), ('tbsp', 'tablespoon'), ('kg', 'kilogram'), ('pt', 'pint'), ('na', 'none'), ('gal', 'gallon'), ('g', 'gram'), ('slices', 'slices'), ('tsp', 'teaspoon'), ('ml', 'milliliter'), ('slice', 'slice'), ('cup', 'cup')], max_length=15),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='platform',
            field=models.CharField(choices=[('Y', 'YouTube'), ('TK', 'TikTok'), ('F', 'Facebook'), ('S', 'Snapchat'), ('I', 'Instagram'), ('TW', 'Twitter')], max_length=2),
        ),
    ]
