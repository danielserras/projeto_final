# Generated by Django 3.1.7 on 2021-04-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_invoice_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='month',
            field=models.DateField(null=True),
        ),
    ]
