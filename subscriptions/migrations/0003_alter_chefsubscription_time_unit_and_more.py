# Generated by Django 4.2.11 on 2024-04-28 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chefsubscription',
            name='time_unit',
            field=models.CharField(choices=[('M', 'Month'), ('Y', 'Year'), ('W', 'Week')], max_length=1),
        ),
        migrations.AlterField(
            model_name='sitesubscription',
            name='time_unit',
            field=models.CharField(choices=[('M', 'Month'), ('Y', 'Year'), ('W', 'Week')], max_length=10),
        ),
    ]
