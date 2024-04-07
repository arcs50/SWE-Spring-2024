# Generated by Django 4.2.11 on 2024-03-27 21:10

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chefsubscription',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='chefsubscription',
            name='time_quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='chefsubscription',
            name='time_unit',
            field=models.CharField(choices=[('M', 'Month'), ('W', 'Week'), ('Y', 'Year')], max_length=1),
        ),
        migrations.AlterField(
            model_name='sitesubscription',
            name='time_unit',
            field=models.CharField(choices=[('M', 'Month'), ('W', 'Week'), ('Y', 'Year')], max_length=10),
        ),
    ]
