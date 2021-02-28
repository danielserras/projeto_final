from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory


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
    availability_starts = forms.DateField()
    availability_ending = forms.DateField()
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=100)
    security_deposit = forms.IntegerField()
    max_capacity = forms.IntegerField(required=True)

    class Meta:
        model = Bedroom
        fields = [
            'allowed_gender',
            'monthly_payment',
            'availability_starts',
            'availability_ending',
            'title',
            'description',
            'security_deposit',
            'max_capacity'
        ]

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

    class Meta:
        model = Property
        fields = [
            'property_type',
            'address',
            'smoke',
            'garden',
            'garage',
            'street_parking',
            'internet',
            'electricity',            
            'water',  
            'gas',
            'pets',
            'overnight_visits',
            'cleaning_services',
            'floor_area']


class BedroomForm(forms.ModelForm):

    be_chairs = forms.BooleanField(required=False, initial=False)
    be_sofa = forms.BooleanField(required=False, initial=False)
    be_sofa_bed = forms.BooleanField(required=False, initial=False)
    be_window = forms.BooleanField(required=False, initial=False)
    num_single_beds = forms.IntegerField(required=True)
    num_double_beds = forms.IntegerField(required=True)
    max_occupacity = forms.IntegerField(required=True)
    be_balcony = forms.BooleanField(required=False, initial=False)
    wardrobe = forms.BooleanField(required=False, initial=False)
    be_desk = forms.BooleanField(required=False, initial=False)
    chest_of_drawers = forms.BooleanField(required=False, initial=False)
    tv = forms.BooleanField(required=False, initial=False)
    heater = forms.BooleanField(required=False, initial=False)
    air_conditioning = forms.BooleanField(required=False, initial=False)
    ensuite_bathroom = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Bedroom
        fields = [
            "be_chairs",
            "be_sofa",
            "be_sofa_bed",
            "be_window",
            "num_single_beds",
            "num_double_beds",
            "max_occupacity",
            "be_balcony",
            "wardrobe",
            "be_desk",
            "chest_of_drawers",
            "tv",
            "heater",
            "air_conditioning",
            "ensuite_bathroom"]


class KitchenForm(forms.ModelForm):
    
    oven = forms.BooleanField(required=False, initial=False)
    fridge = forms.BooleanField(required=False, initial=False)
    k_table = forms.BooleanField(required=False, initial=False)
    laundering_machine = forms.BooleanField(required=False, initial=False)
    freezer = forms.BooleanField(required=False, initial=False)
    k_chairs = forms.BooleanField(required=False, initial=False)
    microwave = forms.BooleanField(required=False, initial=False)
    k_window = forms.BooleanField(required=False, initial=False)
    k_balcony = forms.BooleanField(required=False, initial=False)
    dish_washer = forms.BooleanField(required=False, initial=False)
    dishwasher_machine = forms.BooleanField(required=False, initial=False)
    dryer = forms.BooleanField(required=False, initial=False)
    pans_pots = forms.BooleanField(required=False, initial=False)
    dishes_cutlery = forms.BooleanField(required=False, initial=False)
    cooker = forms.BooleanField(required=False, initial=False)
    class Meta:
        model = Kitchen
        fields = [
            'oven',
            'fridge',
            'k_table',
            'laundering_machine',
            'freezer',
            'k_chairs',
            'microwave',
            'k_window',
            'k_balcony',
            'dish_washer',
            'dishwasher_machine',
            'dryer',
            'pans_pots',
            'dishes_cutlery',
            'cooker',]


class BathroomForm(forms.ModelForm):

    shower = forms.BooleanField(required=False, initial=False)
    bathtub = forms.BooleanField(required=False, initial=False)
    bidet = forms.BooleanField(required=False, initial=False)
    toilet = forms.BooleanField(required=False, initial=False)
    sink = forms.BooleanField(required=False, initial=False)
    b_window = forms.BooleanField(required=False, initial=False)
    class Meta:
        model = Bathroom
        fields = [
            'shower',
            'bathtub',
            'bidet',
            'toilet',
            'sink',
            'b_window']


class LivingroomForm(forms.ModelForm):
    l_sofa = forms.BooleanField(required=False, initial=False)
    l_sofa_bed = forms.BooleanField(required=False, initial=False)
    l_chairs = forms.BooleanField(required=False, initial=False)
    l_window = forms.BooleanField(required=False, initial=False)
    l_table = forms.BooleanField(required=False, initial=False)
    l_desk = forms.BooleanField(required=False, initial=False)
    l_balcony = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Livingroom
        fields = [
            'l_sofa',
            'l_sofa_bed',
            'l_chairs',
            'l_window',
            'l_table',
            'l_desk',
            'l_balcony']

"""class AgreementForm(forms.ModelForm):
    startsDate = forms.DateField()
    endDate = forms.DateField()
    
    class Meta:
        model = Agreement
        fields = [
            'startsDate',
            'endDate'] """ #expandiu-se para dentro do agreement request

class Agreement_Request_Form(forms.ModelForm):

    startsDate = forms.DateField()
    endDate = forms.DateField()
    message = forms.CharField(widget=forms.Textarea, required=False)
    accepted = forms.BooleanField(required=False)

    class Meta:
        model = Agreement_Request
        fields = [
            'associated_room',
            'associated_property',
            'tenant',
            'landlord',
            'startsDate',
            'endDate',
            'message',
            'accepted']
        widgets = {
            'associated_room': forms.HiddenInput(),
            'associated_property': forms.HiddenInput(),
            'tenant': forms.HiddenInput(),
            'landlord': forms.HiddenInput(),
            'accepted': forms.HiddenInput()
        }
        




BedroomFormSet = modelformset_factory(model = Bedroom, form = BedroomForm, extra=1)

KitchenFormSet = modelformset_factory(model = Kitchen, form = KitchenForm, extra=1)

BathroomFormSet = modelformset_factory(model = Bathroom, form = BathroomForm, extra=1)

LivingroomFormSet = modelformset_factory(model = Livingroom, form = LivingroomForm, extra=1)