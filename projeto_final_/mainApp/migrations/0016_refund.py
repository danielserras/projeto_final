# Generated by Django 3.1.7 on 2021-04-23 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0015_auto_20210422_2103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('status', models.BooleanField()),
                ('checkReadLandlord', models.BooleanField()),
                ('landlord', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.landlord')),
                ('tenant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.tenant')),
            ],
        ),
    ]