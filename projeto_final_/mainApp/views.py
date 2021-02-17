from django.shortcuts import render

from django.http import HttpResponse

def index(response):
    return render(response, "mainApp/home.html", {})

def startsAgreement(response):
    return render(response, "mainApp/startsAgreement.html", {})

def profile(responde):
    return render(responde, "mainApp/profile.html", {})