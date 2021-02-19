from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import *
from .forms import CreateUserForm
from django.conf import settings 
from django.core.mail import send_mail
from verify_email.email_handler import send_verification_email


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
            user_first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'Utilizador ' + user_nameStr + ' criado!')

            #confirmation email
            subject = 'UniHouses - Confirmação de crendenciais'
            message = f'Olá {user_first_name}, obrigado por se juntar a nós!'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [user.email, ] 
            send_mail( subject, message, email_from, recipient_list ) 

            return redirect('home_page') #placeholder, alterem depois   

    context = {'form':form} #, 'pform':pform
    return render(request, 'mainApp/register.html', context)


def index(response):
    return render(response, "mainApp/home.html", {})

def startsAgreement(response):
    return render(response, "mainApp/startsAgreementTenent.html", {})

def profile(response):
    return render(response, "mainApp/profile.html", {})
