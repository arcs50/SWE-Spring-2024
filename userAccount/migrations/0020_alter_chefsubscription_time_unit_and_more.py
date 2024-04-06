# Generated by Django 5.0.3 on 2024-04-03 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userAccount", "0019_alter_chefsubscription_time_unit_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chefsubscription",
            name="time_unit",
            field=models.CharField(
                choices=[("W", "Week"), ("M", "Month"), ("Y", "Year")], max_length=1
            ),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="measurement",
            field=models.CharField(
                choices=[
                    ("cup", "cup"),
                    ("g", "gram"),
                    ("lb", "pound"),
                    ("qt", "quart"),
                    ("kg", "kilogram"),
                    ("L", "liter"),
                    ("ml", "milliliter"),
                    ("pt", "pint"),
                    ("gal", "gallon"),
                    ("oz", "ounce"),
                    ("tbsp", "tablespoon"),
                    ("na", "none"),
                    ("tsp", "teaspoon"),
                    ("fl oz", "fluid ounce"),
                ],
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="sitesubscription",
            name="time_unit",
            field=models.CharField(
                choices=[("W", "Week"), ("M", "Month"), ("Y", "Year")], max_length=10
            ),
        ),
        migrations.AlterField(
            model_name="socialmedia",
            name="platform",
            field=models.CharField(
                choices=[
                    ("TW", "Twitter"),
                    ("TK", "TikTok"),
                    ("S", "Snapchat"),
                    ("I", "Instagram"),
                    ("Y", "YouTube"),
                    ("F", "Facebook"),
                ],
                max_length=2,
            ),
        ),
    ]
