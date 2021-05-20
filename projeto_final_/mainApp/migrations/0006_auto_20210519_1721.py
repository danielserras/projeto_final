# Generated by Django 3.1.7 on 2021-05-19 17:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_auto_20210519_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_user',
            name='nif',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(999999999), django.core.validators.MinValueValidator(100000000)]),
        ),
    ]
