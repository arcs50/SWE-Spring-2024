# Generated by Django 4.2.11 on 2024-04-24 23:19

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChefSubscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "time_quantity",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "time_unit",
                    models.CharField(
                        choices=[("M", "Month"), ("Y", "Year"), ("W", "Week")],
                        max_length=1,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=6,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.00"))
                        ],
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "stripe_price_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SiteSubscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("time_quantity", models.PositiveIntegerField()),
                (
                    "time_unit",
                    models.CharField(
                        choices=[("M", "Month"), ("Y", "Year"), ("W", "Week")],
                        max_length=10,
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name="SubscriptionToChef",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("blocked", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="SubscriptionToSite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
