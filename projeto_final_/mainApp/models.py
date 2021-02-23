from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class App_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField(null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
#rever tipo de notação :)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        App_user.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.app_user.save()

class Tenant(App_user):
    app_user = models.OneToOneField(User, on_delete=models.CASCADE)


class Landlord(App_user):
    app_user = models.OneToOneField(User, on_delete=models.CASCADE)
    lord_type = models.CharField(max_length=30)

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



# Create your models here.
