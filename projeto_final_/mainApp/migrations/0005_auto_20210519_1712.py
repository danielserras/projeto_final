# Generated by Django 3.1.7 on 2021-05-19 17:12

import django.core.validators
from django.db import migrations, models
import mainApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_app_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_user',
            name='nif',
            field=models.IntegerField(default=123678482, validators=[django.core.validators.MaxValueValidator(999999999)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='app_user',
            name='image',
            field=models.ImageField(upload_to=mainApp.models.get_profile_image_path),
        ),
    ]
