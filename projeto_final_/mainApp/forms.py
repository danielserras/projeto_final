from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms import modelformset_factory


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
    smoke = forms.BooleanField(required=False, initial=False)
    garden = forms.BooleanField(required=False, initial=False)
    garage = forms.BooleanField(required=False, initial=False)
    street_parking = forms.BooleanField(required=False, initial=False)
    internet = forms.BooleanField(required=False, initial=False)
    electricity = forms.BooleanField(required=False, initial=False)            
    water = forms.BooleanField(required=False, initial=False)                  
    gas = forms.BooleanField(required=False, initial=False)
    pets = forms.BooleanField(required=False, initial=False)
    overnight_visits = forms.BooleanField(required=False, initial=False)
    cleaning_services = forms.BooleanField(required=False, initial=False)
    parking_space = forms.BooleanField(required=False, initial=False)
    floor_area = forms.BooleanField(required=False, initial=False)


BedroomFormSet = modelformset_factory(
    Bedroom,
    fields=(
        "chairs",
        "sofa",
        "sofa_bed",
        "window",
        "num_single_beds",
        "num_double_beds",
        "balcony",
        "wardrobe",
        "desk",
        "chest_of_drawers",
        "tv",
        "heater",
        "air_conditioning",
        "ensuite_bathroom"),
    extra=1)

KitchenFormSet = modelformset_factory(
    Kitchen, 
    fields=(
        "oven",                 
        "dish_washer",
        "window", 
        "fridge",
        "freezer",
        "cooker",
        "dishes_cutlery",
        "pans_pots",
        "washing_machine",
        "dryer",
        "oven"),
    extra=1
)

BathroomFormSet = modelformset_factory(    
    Bathroom, 
    fields=(
        "toilet", 
        "sink",
        "shower",
        "window",
        "bathtub",
        "private_or_shared"),
    extra=1
)

LivingroomFormSet = modelformset_factory(
    Livingroom, 
    fields=(
            "chairs",
            "sofa",
            "sofa_bed",
            "window",
            "table",
            "balcony"),
    extra=1
)




""" class BedroomForm(forms.ModelForm):

    bed = forms.BooleanField(required=False, initial=False)
    chairs = forms.BooleanField(required=False, initial=False)
    window = forms.BooleanField(required=False, initial=False)
    drawer = forms.BooleanField(required=False, initial=False)
    couch = forms.BooleanField(required=False, initial=False)
    wardrobe = forms.BooleanField(required=False, initial=False)
    tv =  forms.BooleanField(required=False, initial=False)
    desk = forms.BooleanField(required=False, initial=False)
    lock = forms.BooleanField(required=False, initial=False) """


""" class KitchenForm(forms.ModelForm):
    
    oven = forms.BooleanField(required=False, initial=False)
    fridge = forms.BooleanField(required=False, initial=False)
    table = forms.BooleanField(required=False, initial=False)
    laundering_machine = forms.BooleanField(required=False, initial=False)
    freezer = forms.BooleanField(required=False, initial=False)
    chairs = forms.BooleanField(required=False, initial=False)
    microwave = forms.BooleanField(required=False, initial=False)
    window = forms.BooleanField(required=False, initial=False)
    balcony = forms.BooleanField(required=False, initial=False)
    dishwasher = forms.BooleanField(required=False, initial=False)
    dishwasher_machine = forms.BooleanField(required=False, initial=False)
    dryer = forms.BooleanField(required=False, initial=False) """


""" class BathroomForm(forms.ModelForm):

    shower = forms.BooleanField(required=False, initial=False)
    bathtub = forms.BooleanField(required=False, initial=False)
    bidet = forms.BooleanField(required=False, initial=False)
    toilet = forms.BooleanField(required=False, initial=False)
    sink = forms.BooleanField(required=False, initial=False)
    window = forms.BooleanField(required=False, initial=False) """


""" class LivingroomForm(forms.ModelForm):
    couch = forms.BooleanField(required=False, initial=False)
    sofa_bed = forms.BooleanField(required=False, initial=False)
    chairs = forms.BooleanField(required=False, initial=False)
    window = forms.BooleanField(required=False, initial=False)
    table = forms.BooleanField(required=False, initial=False)
    desk = forms.BooleanField(required=False, initial=False)
    balcony = forms.BooleanField(required=False, initial=False) """