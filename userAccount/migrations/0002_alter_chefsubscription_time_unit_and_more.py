# Generated by Django 5.0.3 on 2024-03-26 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userAccount", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chefsubscription",
            name="time_unit",
            field=models.CharField(
                choices=[("M", "Month"), ("Y", "Year"), ("W", "Week")], max_length=1
            ),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="measurement",
            field=models.CharField(
                choices=[
                    ("na", "none"),
                    ("oz", "ounce"),
                    ("pt", "pint"),
                    ("cup", "cup"),
                    ("qt", "quart"),
                    ("gal", "gallon"),
                    ("tsp", "teaspoon"),
                    ("g", "gram"),
                    ("ml", "milliliter"),
                    ("kg", "kilogram"),
                    ("L", "liter"),
                    ("fl oz", "fluid ounce"),
                    ("tbsp", "tablespoon"),
                    ("lb", "pound"),
                ],
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="role",
            name="role",
            field=models.CharField(
                choices=[("A", "admin"), ("C", "chef"), ("S", "subscriber")],
                max_length=1,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="sitesubscription",
            name="time_unit",
            field=models.CharField(
                choices=[("M", "Month"), ("Y", "Year"), ("W", "Week")], max_length=10
            ),
        ),
        migrations.AlterField(
            model_name="socialmedia",
            name="platform",
            field=models.CharField(
                choices=[
                    ("F", "Facebook"),
                    ("TK", "TikTok"),
                    ("S", "Snapchat"),
                    ("I", "Instagram"),
                    ("TW", "Twitter"),
                    ("Y", "YouTube"),
                ],
                max_length=2,
            ),
        ),
    ]
