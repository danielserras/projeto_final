# Generated by Django 3.1.7 on 2021-04-18 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_invoice_line_invoice_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice_line',
            old_name='invoice_id',
            new_name='invoice',
        ),
    ]
