# Generated by Django 5.0.2 on 2024-03-27 19:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscriptions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chefsubscription',
            name='chef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscriptiontochef',
            name='chef_subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.chefsubscription'),
        ),
        migrations.AddField(
            model_name='subscriptiontochef',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscriptiontosite',
            name='chef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscriptiontosite',
            name='site_subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.sitesubscription'),
        ),
        migrations.AlterUniqueTogether(
            name='subscriptiontochef',
            unique_together={('subscriber', 'chef_subscription', 'start_date')},
        ),
    ]