from django.urls import path, include
from projeto_final import urls
from django.conf.urls.i18n import i18n_patterns
from . import views

urlpatterns = [
    path('profile/propertiesManagement/listingEditing/<int:property_id>/<int:main_listing_id>', views.main_listing_editing_view, name='mainListingEditing'),
    path('profile/propertiesManagement/listingEditing/<int:property_id>', views.listing_editing_view, name='listingEditing'),
    path('profile/propertiesManagement/propertyEditing/<int:property_id>', views.property_editing_view, name='propertyEditing'),
    path('profile/propertiesManagement/bedroomsEditing/<int:property_id>', views.bedrooms_editing_view, name='bedroomsEditing'),  
    path('profile/propertiesManagement/bathroomsEditing/<int:property_id>', views.bathrooms_editing_view, name='bathroomsEditing'),
    path('profile/propertiesManagement/kitchensEditing/<int:property_id>', views.kitchens_editing_view, name='kitchensEditing'),
    path('profile/propertiesManagement/livingroomsEditing/<int:property_id>', views.livingrooms_editing_view, name='livingroomsEditing'),
    path('profile/propertiesManagement', views.properties_management_view, name='propertiesManagement'),
    path('addProperty', views.introduce_property_view, name='addProperty'),
    path('addProperty/bedroom/', views.introduce_property_view, name='addBedroom'),
    path('addProperty/bathroom/', views.introduce_property_view, name='addBathroom'),
    path('addProperty/kitchen/', views.introduce_property_view, name='addKitchen'),
    path('addProperty/livingroom/', views.introduce_property_view, name='addLivingroom'),
    path('addProperty/listing/', views.introduce_property_view, name='addListing'),
    #path('login', views.login_view, name='login_view'),
    #path('logout', views.logout_view, name='logout_view'),
    #path('register', views.register_view, name='register_view'),
    path('profile', views.profile, name = 'profile'),
    path('emailBody', views.emailBody, name = 'emailBody'),
    path('search', views.search, name='search'),
    path('', views.index, name='index'),
    path('notificationsTenant', views.notificationsTenant, name='notificationsTenant'),
    path('notificationsLandlord', views.notificationsLandlord, name='notificationsLandlord'),
    path('listing/application', views.create_request, name='create_request'),
    path('listing/<int:listing_id>', views.listing, name='listing'),
    path('notificationsLandlord/requestAccepted/<int:request_id>', views.accept_request, name='accept_request'),
    path('notificationsLandlord/requestDenied/<int:request_id>', views.deny_request, name='deny_request'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/changeToRegister', views.changeToRegister, name='changeToRegister'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('login/confirmed', views.deletePopUp, name='deletePopUp'),
    path('profile/renewAgreement', views.renewAgreement, name='renewAgreement'),
    
]

