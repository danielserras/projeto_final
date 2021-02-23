from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

    
class App_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField(null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    #rever tipo de notação :)

class Tenant(models.Model):

    ten_user = models.ForeignKey(App_user, on_delete=models.CASCADE)

class Landlord(models.Model):

    lord_user = models.ForeignKey(App_user, on_delete=models.CASCADE)
    lord_type = models.CharField(max_length=30, default='Particular')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        App_user.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.app_user.save()


class Property(models.Model):
    property_type = models.CharField(max_length=20)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    floor_area = models.IntegerField()              
    max_capacity = models.IntegerField()
    garden = models.BooleanField()
    garage = models.BooleanField()
    street_parking = models.BooleanField()
    internet = models.BooleanField()
    electricity = models.BooleanField()             
    water = models.BooleanField()
    gas = models.BooleanField()
    pets = models.BooleanField()
    overnight_visits = models.BooleanField()
    cleaning_services = models.BooleanField()


class Bathroom(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)
    toilet = models.BooleanField() 
    sink = models.BooleanField()
    shower = models.BooleanField()
    window = models.BooleanField()
    bathtub = models.BooleanField()
    private_or_shared = models.BooleanField()

class Bedroom(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)
    chairs = models.BooleanField()
    sofa = models.BooleanField()
    sofa_bed = models.BooleanField()
    window = models.BooleanField()
    num_single_beds = models.IntegerField()
    num_double_beds = models.IntegerField()
    balcony = models.BooleanField()
    wardrobe = models.BooleanField()
    desk = models.BooleanField()
    chest_of_drawers = models.BooleanField()
    tv = models.BooleanField()
    heater = models.BooleanField()
    air_conditioning = models.BooleanField()
    ensuite_bathroom = models.BooleanField()

class Kitchen(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)
    dish_washer = models.BooleanField()
    window = models.BooleanField()
    fridge = models.BooleanField()
    freezer = models.BooleanField()
    cooker = models.BooleanField()
    dishes_cutlery = models.BooleanField()
    pans_pots = models.BooleanField()
    washing_machine = models.BooleanField()
    dryer = models.BooleanField() 
    oven = models.BooleanField()

class Livingroom(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)
    chairs = models.BooleanField()
    sofa = models.BooleanField()
    sofa_bed = models.BooleanField()
    window = models.BooleanField()
    table = models.BooleanField()
    balcony = models.BooleanField()

class Listing(models.Model):
    allowed_gender = models.CharField(max_length=20)
    monthly_payment = models.IntegerField()
    availability_starts = models.DateField()
    availability_ending = models.DateField()
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    security_deposit = models.IntegerField()    


class Room_listing(Listing):
    associated_room = models.OneToOneField(Bedroom, on_delete = models.CASCADE)

class Property_listing(Listing):
    associated_property = models.OneToOneField(Property, on_delete = models.CASCADE)


class Agreement(models.Model):
    associated_room = models.ForeignKey(Room_listing on_delete=models.CASCADE)
    associated_room = models.models.ForeignKey(Property_listing on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    startsDate = models.DateField()
    endDate = models.DateField()

# Create your models here.
