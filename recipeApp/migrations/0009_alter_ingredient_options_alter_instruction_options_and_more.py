# Generated by Django 4.2.11 on 2024-04-18 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeApp', '0008_ingredient_order_instruction_order_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='instruction',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_image',
            field=models.ImageField(blank=True, upload_to='statics/images/'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement',
            field=models.CharField(choices=[('lb', 'pound'), ('tsp', 'teaspoon'), ('gal', 'gallon'), ('fl oz', 'fluid ounce'), ('g', 'gram'), ('L', 'liter'), ('cup', 'cup'), ('kg', 'kilogram'), ('tbsp', 'tablespoon'), ('oz', 'ounce'), ('qt', 'quart'), ('ml', 'milliliter'), ('na', 'none'), ('pt', 'pint')], max_length=15),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='platform',
            field=models.CharField(choices=[('S', 'Snapchat'), ('F', 'Facebook'), ('I', 'Instagram'), ('TW', 'Twitter'), ('Y', 'YouTube'), ('TK', 'TikTok')], max_length=2),
        ),
    ]
