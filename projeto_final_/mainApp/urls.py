from django.urls import path

from . import views

urlpatterns = [
    path('addListing', views.introduce_property_view, name='addListing'),
    path('login', views.login_view, name='login_view'),
    path('register', views.register_view, name='register_view'),
    path('profile', views.profile, name = 'profile'),
    path('startsAgreement', views.startsAgreement, name='startsAgreement'),
    path('search', views.search, name='search'),
    path('', views.index, name='index'),
    path('notifications', views.notifications, name='notifications'),
    path('listing', views.listing, name='listing')
]
