# Generated by Django 3.1.7 on 2021-04-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0012_payment_warning'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_warning',
            name='timestamp',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
