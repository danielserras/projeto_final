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

class ListingForm(forms.ModelForm):
    
    allowed_gender = forms.CharField(required=True, max_length=25)
    monthly_payment = forms.IntegerField(required=True)
    availabilityStarts = forms.DateField()
    availabilityEnds = forms.DateField()
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=100)
    security_deposit = forms.IntegerField()
    max_capacity = forms.IntegerField(required=True)

class PropertyForm(forms.ModelForm):

    property_type = forms.CharField(required=True, max_length=25)
    address = forms.CharField(required=True, max_length=100)
    #nBedrooms = forms.IntegerField(required=True) 
    #nBathrooms = forms.IntegerField(required=True)

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
    floor_area = forms.BooleanField(required=False, initial=False)


class BedroomForm(forms.ModelForm):
    
    chairs = forms.BooleanField(required=False, initial=False)
    sofa = forms.BooleanField(required=False, initial=False)
    sofa_bed = forms.BooleanField(required=False, initial=False)
    window = forms.BooleanField(required=False, initial=False)
    num_single_beds = forms.IntegerField(required=True)
    num_double_beds = forms.IntegerField(required=True)
    balcony = forms.BooleanField(required=False, initial=False)
    wardrobe = forms.BooleanField(required=False, initial=False)
    desk = forms.BooleanField(required=False, initial=False)
    chest_of_drawers = forms.BooleanField(required=False, initial=False)
    tv = forms.BooleanField(required=False, initial=False)
    heater = forms.BooleanField(required=False, initial=False)
    air_conditioning = forms.BooleanField(required=False, initial=False)
    ensuite_bathroom = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Bedroom
        fields = [
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
            "ensuite_bathroom"]


class KitchenForm(forms.ModelForm):
    
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
    dryer = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Kitchen
        fields = [
            'oven',
            'fridge',
            'table',
            'laundering_machine',
            'freezer',
            'chairs',
            'microwave',
            'window',
            'balcony',
            'dishwasher',
            'dishwasher_machine',
            'dryer']


class BathroomForm(forms.ModelForm):

    shower = forms.BooleanField(required=False, initial=False)
    bathtub = forms.BooleanField(required=False, initial=False)
    bidet = forms.BooleanField(required=False, initial=False)
    toilet = forms.BooleanField(required=False, initial=False)
    sink = forms.BooleanField(required=False, initial=False)
    window = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Bathroom
        fields = [
            'shower',
            'bathtub',
            'bidet',
            'toilet',
            'sink',
            'window']


class LivingroomForm(forms.ModelForm):
    couch = forms.BooleanField(required=False, initial=False)
    sofa_bed = forms.BooleanField(required=False, initial=False)
    chairs = forms.BooleanField(required=False, initial=False)
    window = forms.BooleanField(required=False, initial=False)
    table = forms.BooleanField(required=False, initial=False)
    desk = forms.BooleanField(required=False, initial=False)
    balcony = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Livingroom
        fields = [
            'couch',
            'sofa_bed',
            'chairs',
            'window',
            'table',
            'desk',
            'balcony']

BedroomFormSet = modelformset_factory(model = Bedroom, form = BedroomForm, extra=1)

KitchenFormSet = modelformset_factory(model = Kitchen, form = KitchenForm, extra=1)

BathroomFormSet = modelformset_factory(model = Bathroom, form = BathroomForm, extra=1)

LivingroomFormSet = modelformset_factory(model = Livingroom, form = LivingroomForm, extra=1)