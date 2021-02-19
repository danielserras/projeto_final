from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import *
from .forms import CreateUserForm


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
            return redirect('login') #placeholder
    context = {}
    return render(request,'mainApp/login.html', context) #placeholder


def register_view(request):
    form = CreateUserForm() 
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        pform = ProfileForm(request.POST)
        if form.is_valid() and pform.is_valid():
            user = form.save()
            #pform = p_form.save(commit=False)
            #pform.user = user
            pform.save()
            user_nameStr = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + useruser_nameStr )
            return redirect('home_page') #placeholder, alterem depois   

    context = {'form':form} #, 'pform':pform
    return render(request, 'mainApp/register.html', context)


def index(response):
    return render(response, "mainApp/home.html", {})

def startsAgreement(response):
    return render(response, "mainApp/startsAgreementTenent.html", {})

def profile(response):
    return render(response, "mainApp/profile.html", {})

def search(response):
    return render(response, "mainApp/search.html", {})
