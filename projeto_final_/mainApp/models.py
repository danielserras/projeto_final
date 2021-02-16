from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class App_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField()
    birthDate = models.DateField()
    isVerified = models.BooleanField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        App_user.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.App_user.save()

class Tenant(App_user):
    app_user = models.OneToOneField(User, on_delete=models.CASCADE)


class Landlord(App_user):
    app_user = models.OneToOneField(User, on_delete=models.CASCADE)
    lord_type = models.CharField(max_length=30)

# Create your models here.
