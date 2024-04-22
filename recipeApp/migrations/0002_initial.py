# Generated by Django 4.2.11 on 2024-04-19 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipeApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmedia',
            name='chef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='chef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rating',
            name='rater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rating',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeApp.recipe'),
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='billing_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeApp.address'),
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='instruction',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeApp.recipe'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeApp.recipe'),
        ),
        migrations.AddField(
            model_name='grocerylist',
            name='ingredients',
            field=models.ManyToManyField(to='recipeApp.ingredient'),
        ),
        migrations.AddField(
            model_name='grocerylist',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeApp.comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeApp.recipe'),
        ),
        migrations.AddField(
            model_name='collection',
            name='recipes',
            field=models.ManyToManyField(to='recipeApp.recipe'),
        ),
        migrations.AddField(
            model_name='chefprofile',
            name='chef',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookmarkedrecipes',
            name='recipe',
            field=models.ManyToManyField(to='recipeApp.recipe'),
        ),
        migrations.AddField(
            model_name='bookmarkedrecipes',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='recipe',
            unique_together={('chef', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('recipe', 'rater')},
        ),
    ]
