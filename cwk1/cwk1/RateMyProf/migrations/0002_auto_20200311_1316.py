# Generated by Django 3.0.3 on 2020-03-11 13:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RateMyProf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='Rating',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
