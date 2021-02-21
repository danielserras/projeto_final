from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import App_user


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = App_user
        fields = ['phoneNumber', 'birthDate',]

class PropertyForm(forms.ModelForm):

    property_name = forms.CharField(required=True, max_length=50)
    property_type = forms.CharField(required=True, max_length=25)
    address = forms.CharField(required=True, max_length=100)
    rent = forms.IntegerField(required=True)
    max_capacity = forms.IntegerField(required=True)
    nBedrooms = forms.IntegerField(required=True)
    nBathrooms = forms.IntegerField(required=True)
    deposit_fee = forms.IntegerField(required=True)

    #booleans
    smoke = forms.BooleanField(required=False)
    garden = forms.BooleanField(required=False)
    garage = forms.BooleanField(required=False)
    street_parking = forms.BooleanField(required=False)
    internet = forms.BooleanField(required=False)
    electricity = forms.BooleanField(required=False)            #WTF??
    water = forms.BooleanField(required=False)                  #WTF??
    gas = forms.BooleanField(required=False)
    pets = forms.BooleanField(required=False)
    overnight_visits = forms.BooleanField(required=False)
    cleaning_services = forms.BooleanField(required=False)
    parking_space = forms.BooleanField(required=False)

    
class BedroomForm(forms.ModelForm):

    bed = forms.BooleanField(required=False)
    chair = forms.BooleanField(required=False)
    window = forms.BooleanField(required=False)
    drawer = forms.BooleanField(required=False)
    couch = forms.BooleanField(required=False)
    wardrobe = forms.BooleanField(required=False)
    tv =  forms.BooleanField(required=False)
    desk = forms.BooleanField(required=False)
    lock = forms.BooleanField(required=False)


class KitchenForm(forms.ModelForm):
    
    oven = forms.BooleanField(required=False)
    fridge = forms.BooleanField(required=False)
    table = forms.BooleanField(required=False)
    laundering_machine = forms.BooleanField(required=False)
    freezer = forms.BooleanField(required=False)
    chairs = forms.BooleanField(required=False)
    microwave = forms.BooleanField(required=False)
    window = forms.BooleanField(required=False)
    balcony = forms.BooleanField(required=False)
    dishwasher = forms.BooleanField(required=False)
    dishwasher_machine = forms.BooleanField(required=False)
    dryer = forms.BooleanField(required=False)


class BathroomForm(models.ModelForm):

    shower = forms.BooleanField(required=False)
    bathtub = forms.BooleanField(required=False)
    bidet = forms.BooleanField(required=False)
    toilet = forms.BooleanField(required=False)
    sink = forms.BooleanField(required=False)
    window = forms.BooleanField(required=False)


class LivingroomForm(models.ModelForm):
    couch = forms.BooleanField(required=False)
    sofa_bed = forms.BooleanField(required=False)
    chairs = forms.BooleanField(required=False)
    window = forms.BooleanField(required=False)
    table = forms.BooleanField(required=False)
    desk = forms.BooleanField(required=False)
    balcony = forms.BooleanField(required=False)