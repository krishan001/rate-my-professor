# Generated by Django 3.0.3 on 2020-02-26 13:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RateMyProf', '0009_auto_20200226_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduleinstance',
            name='Year',
            field=models.IntegerField(default=2020, validators=[django.core.validators.MinValueValidator(1904), django.core.validators.MaxValueValidator(2020)]),
        ),
    ]
