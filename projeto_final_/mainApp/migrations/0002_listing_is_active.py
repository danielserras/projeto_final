# Generated by Django 3.1.7 on 2021-03-15 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_active',

            field=models.BooleanField(default=0),
    )]
