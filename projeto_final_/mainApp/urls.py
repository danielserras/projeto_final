from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.profile, name = 'profile'),
    path('startsAgreement', views.startsAgreement, name='startsAgreement'),
    path('', views.index, name='index'),
]
