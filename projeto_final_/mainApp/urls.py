from django.urls import path, include
from projeto_final import urls
from . import views

urlpatterns = [
    path('profile/propertiesManagement/listingEdit/<int:property_id>', views.listing_edit_view, name='listingEdit'),
    path('profile/propertiesManagement/propertyEdit/<int:property_id>', views.property_edit_view, name='propertyEdit'),
    path('profile/propertiesManagement', views.properties_management_view, name='propertiesManagement'),
    path('addProperty', views.introduce_property_view, name='addProperty'),
    path('addProperty/bedroom/', views.introduce_property_view, name='addBedroom'),
    path('addProperty/bathroom/', views.introduce_property_view, name='addBathroom'),
    path('addProperty/kitchen/', views.introduce_property_view, name='addKitchen'),
    path('addProperty/livingroom/', views.introduce_property_view, name='addLivingroom'),
    path('addProperty/listing/', views.introduce_property_view, name='addListing'),
    path('login', views.login_view, name='login_view'),
    #path('logout', views.logout_view, name='logout_view'),
    path('register', views.register_view, name='register_view'),
    path('profile', views.profile, name = 'profile'),
    path('startsAgreement', views.startsAgreement, name='startsAgreement'),
    path('search', views.search, name='search'),
    path('', views.index, name='index'),
    path('notificationsTenant', views.notificationsTenant, name='notificationsTenant'),
    path('notificationsLandlord', views.notificationsLandlord, name='notificationsLandlord'),
    path('listing/application', views.create_request, name='create_request'),
    path('listing/<int:listing_id>', views.listing, name='listing'),
    path('accounts/', include('django.contrib.auth.urls')),
]
