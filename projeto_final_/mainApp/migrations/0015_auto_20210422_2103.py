# Generated by Django 3.1.7 on 2021-04-22 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0014_auto_20210421_1747'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agreement_request',
            old_name='checkRead',
            new_name='checkReadLandlord',
        ),
        migrations.AddField(
            model_name='agreement_request',
            name='checkReadTenant',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
    ]