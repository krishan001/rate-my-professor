# Generated by Django 3.0.3 on 2020-02-26 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RateMyProf', '0006_auto_20200226_1302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='studentNAme',
            new_name='studentName',
        ),
    ]
