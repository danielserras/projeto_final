from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import *
from .forms import *
from django.conf import settings 
from django.core.mail import send_mail
from verify_email.email_handler import send_verification_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('home_page') #placeholder, alterem depois
        else:
            messages.info(request, 'Username ou password incorretos')
            return redirect('index') #placeholder
    context = {}
    return render(request,'mainApp/login.html', context) #placeholder


def register_view(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        pform = ProfileForm(request.POST)

        if form.is_valid() and pform.is_valid():
            inactive_user = send_verification_email(request, form)
            #user = form.save()
            app_user_object = App_user.objects.get(user_id=inactive_user)
            app_user_object.phoneNumber = pform.cleaned_data['phoneNumber']
            app_user_object.birthDate = pform.cleaned_data['birthDate']
            app_user_object.save()
            #pform = p_form.save(commit=False)
            #pform.user = user
            #pform.save()
            user_nameStr = form.cleaned_data.get('username')
            user_first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'Utilizador ' + user_nameStr + ' criado!')

            return redirect('search') #placeholder, alterem depois   

    context = {'form':form} #, 'pform':pform
    return render(request, 'mainApp/register.html', context)

""" def introduce_property_view (request):

    if request.method == 'POST':
        prop_form = PropertyForm(request.POST)
        bath_form = BathroomForm(request.POST)
        kitchen_form = KitchenForm(request.POST)
        live_form = LivingroomForm(request.POST)
        bed_form = BedroomForm(request.POST)

        form_list = [prop_form, bath_form, kitchen_form, live_form, bed_form]

        for f in form_list:
            if f.is_bound:

                if f == prop_form:
                    if f.is_valid():
                        

                if f == bath_form:
                    

                if f == kitchen_form:


                if f == live_form:


                if f == bed_form:
 """

def index(response):
    return render(response, "mainApp/home.html", {})

def startsAgreement(response):
    return render(response, "mainApp/startsAgreementTenent.html", {})
    #return render(response, "mainApp/sendAgreementLandlord.html", {})

def profile(response):
    return render(response, "mainApp/profile.html", {})

def search(response):
    return render(response, "mainApp/search.html", {})
