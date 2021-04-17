# Generated by Django 3.1.7 on 2021-04-15 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mainApp.models


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
            name='Bedroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('be_chairs', models.BooleanField()),
                ('be_sofa', models.BooleanField()),
                ('be_sofa_bed', models.BooleanField()),
                ('be_window', models.BooleanField()),
                ('num_single_beds', models.IntegerField()),
                ('num_double_beds', models.IntegerField()),
                ('max_occupancy', models.IntegerField()),
                ('be_balcony', models.BooleanField()),
                ('wardrobe', models.BooleanField()),
                ('be_desk', models.BooleanField()),
                ('chest_of_drawers', models.BooleanField()),
                ('tv', models.BooleanField()),
                ('heater', models.BooleanField()),
                ('air_conditioning', models.BooleanField()),
                ('lock', models.BooleanField()),
                ('ensuite_bathroom', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ImageAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
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
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=280)),
                ('security_deposit', models.IntegerField()),
                ('max_capacity', models.IntegerField()),
                ('listing_type', models.CharField(max_length=20)),
                ('is_active', models.BooleanField()),
                ('album', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ListingAlbum', to='mainApp.imagealbum')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('latitude', models.DecimalField(decimal_places=14, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=14, max_digits=20)),
                ('bedrooms_num', models.IntegerField()),
                ('listing_type', models.CharField(max_length=20)),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.landlord')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(blank=True, max_length=100, null=True)),
                ('min_search', models.IntegerField(default=500)),
                ('max_search', models.IntegerField(default=1200)),
                ('ten_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainApp.app_user')),
            ],
        ),
        migrations.CreateModel(
            name='Room_listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('associated_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.bedroom')),
                ('main_listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='r_main', to='mainApp.listing')),
            ],
        ),
        migrations.CreateModel(
            name='Property_listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('associated_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.property')),
                ('main_listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='p_main', to='mainApp.listing')),
            ],
        ),
        migrations.CreateModel(
            name='Livingroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l_chairs', models.BooleanField()),
                ('l_sofa', models.BooleanField()),
                ('l_sofa_bed', models.BooleanField()),
                ('l_window', models.BooleanField()),
                ('l_table', models.BooleanField()),
                ('l_balcony', models.BooleanField()),
                ('l_desk', models.BooleanField()),
                ('associated_property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='livingroom', to='mainApp.property')),
            ],
        ),
        migrations.CreateModel(
            name='Kitchen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_washer', models.BooleanField()),
                ('k_window', models.BooleanField()),
                ('fridge', models.BooleanField()),
                ('freezer', models.BooleanField()),
                ('cooker', models.BooleanField()),
                ('dishes_cutlery', models.BooleanField()),
                ('pans_pots', models.BooleanField()),
                ('dishwasher_machine', models.BooleanField()),
                ('dryer', models.BooleanField()),
                ('oven', models.BooleanField()),
                ('k_table', models.BooleanField()),
                ('laundering_machine', models.BooleanField()),
                ('k_chairs', models.BooleanField()),
                ('microwave', models.BooleanField()),
                ('k_balcony', models.BooleanField()),
                ('associated_property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kitchen', to='mainApp.property')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('is_cover', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to=mainApp.models.get_upload_path)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mainApp.imagealbum')),
            ],
        ),
        migrations.AddField(
            model_name='bedroom',
            name='associated_property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bedroom', to='mainApp.property'),
        ),
        migrations.CreateModel(
            name='Bathroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toilet', models.BooleanField()),
                ('sink', models.BooleanField()),
                ('shower', models.BooleanField()),
                ('b_window', models.BooleanField()),
                ('bathtub', models.BooleanField()),
                ('bidet', models.BooleanField()),
                ('associated_property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bathroom', to='mainApp.property')),
            ],
        ),
        migrations.CreateModel(
            name='Agreement_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startsDate', models.DateField()),
                ('endDate', models.DateField()),
                ('message', models.TextField(blank=True, null=True)),
                ('accepted', models.BooleanField(blank=True, null=True)),
                ('dateOfRequest', models.DateTimeField()),
                ('associated_property_listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.property_listing')),
                ('associated_room_listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.room_listing')),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.landlord')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startsDate', models.DateField()),
                ('endDate', models.DateField()),
                ('associated_property_listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.property_listing')),
                ('associated_room_listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.room_listing')),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.landlord')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.tenant')),
            ],
        ),
    ]
