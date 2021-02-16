from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class App_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField()
    birthDate = models.DateField()
    isVerified = models.BooleanField()

class Tenant(App_user):
    app_user = models.OneToOneField(User, on_delete=models.CASCADE)


class Landlord(App_user):
    app_user = models.OneToOneField(User, on_delete=models.CASCADE)
    lord_type = models.CharField(max_length=30)

# Create your models here.
