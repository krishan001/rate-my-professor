# Generated by Django 3.0.3 on 2020-02-24 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RateMyProf', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='professor',
        ),
        migrations.RemoveField(
            model_name='module',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='module',
            name='year',
        ),
        migrations.RemoveField(
            model_name='prof',
            name='profRating',
        ),
    ]
