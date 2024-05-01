# Generated by Django 4.2.11 on 2024-04-29 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0001_initial'),
    ]

    operations = [
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
            model_name='chefsubscription',
            name='chef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='subscriptiontochef',
            unique_together={('subscriber', 'chef_subscription', 'start_date')},
        ),
        migrations.AlterUniqueTogether(
            name='chefsubscription',
            unique_together={('chef', 'title', 'time_quantity', 'time_unit', 'price')},
        ),
    ]
