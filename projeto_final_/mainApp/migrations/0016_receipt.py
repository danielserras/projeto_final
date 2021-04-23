# Generated by Django 3.1.7 on 2021-04-23 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0015_auto_20210422_2103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.invoice')),
            ],
        ),
    ]
