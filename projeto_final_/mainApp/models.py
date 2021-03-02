from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def get_upload_path(instance, filename):
    path = instance.album.ListingAlbum.id
    return f'{path}/{filename}'


class App_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField(null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)

class Tenant(models.Model):
    ten_user = models.OneToOneField(App_user, on_delete=models.CASCADE)
class Landlord(models.Model):

    lord_user = models.OneToOneField(App_user, on_delete=models.CASCADE)
    lord_type = models.CharField(max_length=30, default='Particular')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        App_user.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.app_user.save()


class ImageAlbum(models.Model):
    name = models.CharField(max_length=250)


class Image(models.Model):
    name = models.CharField(max_length=250)
    is_cover = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_upload_path)
    album = models.ForeignKey(ImageAlbum, related_name="images", on_delete=models.CASCADE)


class Property(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    floor_area = models.IntegerField()              
    garden = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)
    street_parking = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    electricity = models.BooleanField(default=False)             
    water = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    overnight_visits = models.BooleanField(default=False)
    cleaning_services = models.BooleanField(default=False)
    smoke = models.BooleanField(default=False)


class Bathroom(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)
    toilet = models.BooleanField() 
    sink = models.BooleanField()
    shower = models.BooleanField()
    b_window = models.BooleanField()
    bathtub = models.BooleanField()
    bidet = models.BooleanField()


class Bedroom(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)
    be_chairs = models.BooleanField(default=False)
    be_sofa = models.BooleanField(default=False)
    be_sofa_bed = models.BooleanField(default=False)
    be_window = models.BooleanField(default=False)
    num_single_beds = models.IntegerField(default=False)
    num_double_beds = models.IntegerField(default=False)
    max_occupacity = models.IntegerField(default=False)
    be_balcony = models.BooleanField(default=False)
    wardrobe = models.BooleanField(default=False)
    be_desk = models.BooleanField(default=False)
    chest_of_drawers = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    heater = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    ensuite_bathroom = models.BooleanField(default=False)

class Kitchen(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)
    dish_washer = models.BooleanField(default=False)
    k_window = models.BooleanField(default=False)
    fridge = models.BooleanField(default=False)
    freezer = models.BooleanField(default=False)
    cooker = models.BooleanField(default=False)
    dishes_cutlery = models.BooleanField(default=False)
    pans_pots = models.BooleanField(default=False)
    dishwasher_machine = models.BooleanField(default=False)
    dryer = models.BooleanField(default=False) 
    oven = models.BooleanField(default=False)
    k_table = models.BooleanField(default=False)
    laundering_machine = models.BooleanField(default=False)
    k_chairs = models.BooleanField(default=False)
    microwave = models.BooleanField(default=False)
    k_balcony = models.BooleanField(default=False)



class Livingroom(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)
    l_chairs = models.BooleanField(default=False)
    l_sofa = models.BooleanField(default=False)
    l_sofa_bed = models.BooleanField(default=False)
    l_window = models.BooleanField(default=False)
    l_table = models.BooleanField(default=False)
    l_balcony = models.BooleanField(default=False)
    l_desk = models.BooleanField(default=False)

class Listing(models.Model):
    allowed_gender = models.CharField(max_length=20)
    monthly_payment = models.IntegerField()
    availability_starts = models.DateField()
    availability_ending = models.DateField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=280)
    security_deposit = models.IntegerField()
    max_capacity = models.IntegerField()
    listing_type = models.CharField(max_length=20)
    album = models.OneToOneField(ImageAlbum, related_name="ListingAlbum", on_delete=models.CASCADE, blank=True, null=True)



class Room_listing(models.Model):
    main_listing = models.OneToOneField(Listing, on_delete = models.CASCADE, related_name='r_main')
    associated_room = models.ForeignKey(Bedroom, on_delete = models.CASCADE)

class Property_listing(models.Model):
    main_listing = models.OneToOneField(Listing, on_delete = models.CASCADE, related_name='p_main')
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)

class Agreement(models.Model):
    associated_room = models.ForeignKey(Room_listing, null=True, on_delete=models.CASCADE)
    associated_property = models.ForeignKey(Property_listing, null=True, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    startsDate = models.DateField()
    endDate = models.DateField()

class Agreement_Request(models.Model):
    associated_room = models.ForeignKey(Room_listing, null=True, on_delete=models.CASCADE)
    associated_property = models.ForeignKey(Property_listing, null=True, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    startsDate = models.DateField()
    endDate = models.DateField()
    message = models.TextField(null=True, blank=True)
    accepted = models.BooleanField(null=True, blank=True)
# Create your models here.
