# Generated by Django 4.2.11 on 2024-04-10 19:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0004_chefsubscription_active_and_more'),
    ]

    operations = [
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
        migrations.AlterUniqueTogether(
            name='chefsubscription',
            unique_together={('chef', 'title', 'time_quantity', 'time_unit', 'price')},
        ),
    ]
