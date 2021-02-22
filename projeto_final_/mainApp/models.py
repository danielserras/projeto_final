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

    tenant_user = models.ForeignKey(App_user, on_delete=models.CASCADE, primary_key=True)
    pass


class Landlord(models.Model):
    
    lord_user = models.ForeignKey(App_user, on_delete=models.CASCADE, primary_key=True)
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
    floor_area = models.IntegerField()              # que eh isto?
    max_capacity =  models.IntegerField()
    garden = models.BooleanField()
    garage = models.BooleanField()
    street_parking = models.BooleanField()
    internet = models.BooleanField()
    electricity = models.BooleanField()             # WTF??
    water = models.BooleanField()                   # WTF??
    gas = models.BooleanField()
    pets = models.BooleanField()
    overnight_visits = models.BooleanField()
    cleaning_services = models.BooleanField()


class Bathroom(models.Model):
    associatedProperty = models.ForeignKey(Property, on_delete = models.CASCADE)
    toilet = models.BooleanField()
    sink = models.BooleanField()
    shower = models.BooleanField()
    window = models.BooleanField()
    bathtub = models.BooleanField()
    privateOrshared = models.BooleanField()

# Create your models here.
