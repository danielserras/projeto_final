# Generated by Django 3.1.2 on 2021-02-23 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.IntegerField(blank=True, null=True)),
                ('birthDate', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lord_type', models.CharField(default='Particular', max_length=30)),
                ('lord_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.app_user')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.app_user')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('floor_area', models.IntegerField()),
                ('max_capacity', models.IntegerField()),
                ('garden', models.BooleanField()),
                ('garage', models.BooleanField()),
                ('street_parking', models.BooleanField()),
                ('internet', models.BooleanField()),
                ('electricity', models.BooleanField()),
                ('water', models.BooleanField()),
                ('gas', models.BooleanField()),
                ('pets', models.BooleanField()),
                ('overnight_visits', models.BooleanField()),
                ('cleaning_services', models.BooleanField()),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.landlord')),
            ],
        ),
        migrations.CreateModel(
            name='Livingroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chairs', models.BooleanField()),
                ('sofa', models.BooleanField()),
                ('sofa_bed', models.BooleanField()),
                ('window', models.BooleanField()),
                ('table', models.BooleanField()),
                ('balcony', models.BooleanField()),
                ('associated_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.property')),
            ],
        ),
        migrations.CreateModel(
            name='Kitchen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_washer', models.BooleanField()),
                ('window', models.BooleanField()),
                ('fridge', models.BooleanField()),
                ('freezer', models.BooleanField()),
                ('cooker', models.BooleanField()),
                ('dishes_cutlery', models.BooleanField()),
                ('pans_pots', models.BooleanField()),
                ('washing_machine', models.BooleanField()),
                ('dryer', models.BooleanField()),
                ('oven', models.BooleanField()),
                ('associated_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.property')),
            ],
        ),
        migrations.CreateModel(
            name='Bedroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chairs', models.BooleanField()),
                ('sofa', models.BooleanField()),
                ('sofa_bed', models.BooleanField()),
                ('window', models.BooleanField()),
                ('num_single_beds', models.IntegerField()),
                ('num_double_beds', models.IntegerField()),
                ('balcony', models.BooleanField()),
                ('wardrobe', models.BooleanField()),
                ('desk', models.BooleanField()),
                ('chest_of_drawers', models.BooleanField()),
                ('tv', models.BooleanField()),
                ('heater', models.BooleanField()),
                ('air_conditioning', models.BooleanField()),
                ('ensuite_bathroom', models.BooleanField()),
                ('associated_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.property')),
            ],
        ),
        migrations.CreateModel(
            name='Bathroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toilet', models.BooleanField()),
                ('sink', models.BooleanField()),
                ('shower', models.BooleanField()),
                ('window', models.BooleanField()),
                ('bathtub', models.BooleanField()),
                ('private_or_shared', models.BooleanField()),
                ('associated_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.property')),
            ],
        ),
    ]
