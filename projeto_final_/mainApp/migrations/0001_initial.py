# Generated by Django 3.1.2 on 2021-02-26 23:59

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
                ('lord_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainApp.app_user')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allowed_gender', models.CharField(max_length=20)),
                ('monthly_payment', models.IntegerField()),
                ('availability_starts', models.DateField()),
                ('availability_ending', models.DateField()),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=20)),
                ('security_deposit', models.IntegerField()),
                ('max_capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainApp.app_user')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('floor_area', models.IntegerField()),
                ('garden', models.BooleanField(default=False)),
                ('garage', models.BooleanField(default=False)),
                ('street_parking', models.BooleanField(default=False)),
                ('internet', models.BooleanField(default=False)),
                ('electricity', models.BooleanField(default=False)),
                ('water', models.BooleanField(default=False)),
                ('gas', models.BooleanField(default=False)),
                ('pets', models.BooleanField(default=False)),
                ('overnight_visits', models.BooleanField(default=False)),
                ('cleaning_services', models.BooleanField(default=False)),
                ('smoke', models.BooleanField(default=False)),
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
                ('desk', models.BooleanField()),
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
                ('dishwasher_machine', models.BooleanField()),
                ('dryer', models.BooleanField()),
                ('oven', models.BooleanField()),
                ('table', models.BooleanField()),
                ('laundering_machine', models.BooleanField()),
                ('chairs', models.BooleanField()),
                ('microwave', models.BooleanField()),
                ('balcony', models.BooleanField()),
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
                ('max_occupacity', models.IntegerField()),
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
                ('bidet', models.BooleanField()),
                ('associated_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.property')),
            ],
        ),
        migrations.CreateModel(
            name='Room_listing',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainApp.listing')),
                ('associated_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.bedroom')),
                ('main_listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='r_main', to='mainApp.listing')),
            ],
            bases=('mainApp.listing',),
        ),
        migrations.CreateModel(
            name='Property_listing',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainApp.listing')),
                ('associated_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.property')),
                ('main_listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='p_main', to='mainApp.listing')),
            ],
            bases=('mainApp.listing',),
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startsDate', models.DateField()),
                ('endDate', models.DateField()),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.landlord')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.tenant')),
                ('associated_property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.property_listing')),
                ('associated_room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.room_listing')),
            ],
        ),
    ]
