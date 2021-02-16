from django.shortcuts import render

from django.http import HttpResponse

def index(response):
    return render(response, "mainApp/base.html", {})

def home(response):
    return render(response, "mainApp/home.html", {})
