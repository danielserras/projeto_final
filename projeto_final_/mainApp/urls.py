from django.urls import path

from . import views

urlpatterns = [
    path('profile/listingsManagement', views.listing_management_view, name='listings_management'),
    path('addProperty', views.introduce_property_view, name='addProperty'),
    path('addProperty/bedroom/', views.introduce_property_view, name='addBedroom'),
    path('addProperty/bathroom/', views.introduce_property_view, name='addBathroom'),
    path('addProperty/kitchen/', views.introduce_property_view, name='addKitchen'),
    path('addProperty/livingroom/', views.introduce_property_view, name='addLivingroom'),
    path('addProperty/listing/', views.introduce_property_view, name='addListing'),
    path('login', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('register', views.register_view, name='register_view'),
    path('profile', views.profile, name = 'profile'),
    path('startsAgreement', views.startsAgreement, name='startsAgreement'),
    path('search', views.search, name='search'),
    path('', views.index, name='index'),
    path('notificationsTenent', views.notificationsTenent, name='notificationsTenent'),
    path('notificationsLandlord', views.notificationsLandlord, name='notificationsLandlord'),
    path('notifications3', views.notifications3, name='notifications3'),
    path('listing/application', views.create_request, name='create_request'),
    path('listing/<int:listing_id>', views.listing, name='listing')
]
