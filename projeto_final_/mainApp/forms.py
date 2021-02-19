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
