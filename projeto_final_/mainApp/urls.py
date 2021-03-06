from django.urls import path

from . import views

urlpatterns = [
    path('addProperty', views.introduce_property_view, name='addProperty'),
    path('addProperty/bedroom/', views.introduce_property_view, name='addBedroom'),
    path('addProperty/bathroom/', views.introduce_property_view, name='addBathroom'),
    path('addProperty/kitchen/', views.introduce_property_view, name='addKitchen'),
    path('addProperty/livingroom/', views.introduce_property_view, name='addLivingroom'),
    path('addProperty/listing/', views.introduce_property_view, name='addListing'),
    path('addProperty/album/', views.introduce_property_view, name='addAlbum'),
    path('login', views.login_view, name='login_view'),
    path('register', views.register_view, name='register_view'),
    path('profile', views.profile, name = 'profile'),
    path('startsAgreement', views.startsAgreement, name='startsAgreement'),
    path('search', views.search, name='search'),
    path('', views.index, name='index'),
    path('notifications', views.notifications, name='notifications'),
    path('notifications2', views.notifications2, name='notifications2'),
    path('notifications3', views.notifications3, name='notifications3'),
    path('intent', views.intent, name='intent'),
    path('listing/<int:listing_id>', views.listing, name='listing')
]
