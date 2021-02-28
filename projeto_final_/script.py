#exec(open('script.py').read())
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

print("hello world")
user