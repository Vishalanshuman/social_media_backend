# Generated by Django 5.1.2 on 2024-10-18 14:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recipes.recipe')),
            ],
            options={
                'unique_together': {('recipe', 'customer')},
            },
        ),
    ]
