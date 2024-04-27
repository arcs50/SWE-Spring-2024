# Generated by Django 4.1 on 2024-04-25 17:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipeApp", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="measurement",
            field=models.CharField(
                choices=[
                    ("pt", "pint"),
                    ("cup", "cup"),
                    ("g", "gram"),
                    ("tsp", "teaspoon"),
                    ("lb", "pound"),
                    ("tbsp", "tablespoon"),
                    ("slices", "slices"),
                    ("fl oz", "fluid ounce"),
                    ("oz", "ounce"),
                    ("L", "liter"),
                    ("qt", "quart"),
                    ("gal", "gallon"),
                    ("na", "none"),
                    ("kg", "kilogram"),
                    ("slice", "slice"),
                    ("ml", "milliliter"),
                ],
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="socialmedia",
            name="platform",
            field=models.CharField(
                choices=[
                    ("F", "Facebook"),
                    ("S", "Snapchat"),
                    ("I", "Instagram"),
                    ("TW", "Twitter"),
                    ("TK", "TikTok"),
                    ("Y", "YouTube"),
                ],
                max_length=2,
            ),
        ),
    ]
