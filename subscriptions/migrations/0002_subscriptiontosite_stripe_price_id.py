# Generated by Django 4.2.11 on 2024-04-28 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptiontosite",
            name="stripe_price_id",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
