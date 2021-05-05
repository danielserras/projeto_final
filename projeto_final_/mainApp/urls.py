from django.urls import path, include
from projeto_final import urls
from django.conf.urls.i18n import i18n_patterns
from . import views

urlpatterns = [
    path('profile/chats', views.chat_list_view, name='chatsList'),
    path('profile/propertiesManagement/listingEditing/<int:property_id>/<int:main_listing_id>/removeImage/<int:image_id>', views.remove_image_view, name='removeImage'),
    path('profile/propertiesManagement/listingEditing/deleteListing/<int:property_id>/<int:main_listing_id>', views.delete_listing_view, name='deleteListing'),
    path('profile/propertiesManagement/listingEditing/createListing/<int:property_id>', views.create_listing_view, name='createListing'),
    path('profile/propertiesManagement/listingEditing/<int:property_id>/<int:main_listing_id>', views.listing_editing_view, name='listingEditing'),
    path('profile/propertiesManagement/listingEditing/<int:property_id>', views.listings_management_view, name='listingsManagement'),
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
    path('i18n/', include('django.conf.urls.i18n')),
    path('login/confirmed', views.deletePopUp, name='deletePopUp'),
    path('profile/renewAgreement', views.renewAgreement, name='renewAgreement'),
    path('landLord', views.landlord, name='landlord'),
    path('tenant', views.tenant, name='tenant'),
    path('profile/manageAgreements', views.manage_agreements_view, name='manage_agreements_view'),
    path('profile/manageAgreementsTenant', views.manageAgreementsTenant, name='manageAgreementsTenant'),
    path('invoice', views.get_invoice_pdf, name='get_invoice_pdf'),
    path('sendInvoice', views.send_invoice, name='send_invoice'),
    path('sendPaymentWarning', views.send_payment_warning, name='send_payment_warning'),
    path('invoicesLandlord', views.invoicesLandlord, name='invoicesLandlord'),
    path('invoicesTenant', views.invoicesTenant, name='invoicesTenant'),
    path('profile/agreementDeleted', views.deleteAgreement, name='deleteAgreement'),
    path('profile/accountDeleted', views.delete_account, name='delete_account'),
    path('listing/requestPop', views.requestPop, name='requestPop'),
    path('notificationsLandlord/read/<int:id_req>', views.checkReadLandlord, name='checkReadLandlord'),
    path('notificationsTenant/read/<int:id_req>', views.checkReadTenant, name='checkReadTenant'),
    path('notificationsLandlord/readRef/<int:id_ref>', views.checkReadLandlordRef, name='checkReadLandlordRef'),
    path('notificationsLandlord/readInv/<int:id_inv>', views.checkReadTenantInvoice, name='checkReadTenantInvoice'),
    path('notificationsLandlord/readWarn/<int:id_warn>', views.checkReadTenantWarning, name='checkReadTenantWarning'),
    path('profile/delPopUpDuePayment', views.deletePopUpDuePayment, name='deletePopUpDuePayment'),
    path('receipts', views.receipts, name='receipts'),
    path('reasons', views.reasons, name='reasons'),
    path('receipt', views.get_receipt_pdf, name='get_receipt_pdf'),
]

