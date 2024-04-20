# Generated by Django 4.2.11 on 2024-04-17 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_alter_chefsubscription_time_unit_and_more'),
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
    ]
