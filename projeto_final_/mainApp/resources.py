from django.contrib.auth.models import User
from mainApp.models import *
from import_export import resources


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class AppUserResource(resources.ModelResource):
    class Meta:
        model = App_user

class TenantResource(resources.ModelResource):
    class Meta:
        model = Tenant

class LandlordResource(resources.ModelResource):
    class Meta:
        model = Landlord

class ImageAlbumResource(resources.ModelResource):
    class Meta:
        model = ImageAlbum

class ImageResource(resources.ModelResource):
    class Meta:
        model = Image

class PropertyResource(resources.ModelResource):
    class Meta:
        model = Property

class BathroomResource(resources.ModelResource):
    class Meta:
        model = Image

class BedroomResource(resources.ModelResource):
    class Meta:
        model = Bedroom

class KitchenResource(resources.ModelResource):
    class Meta:
        model = Kitchen

class LivingroomResource(resources.ModelResource):
    class Meta:
        model = Livingroom

class ListingResource(resources.ModelResource):
    class Meta:
        model = Listing

class Room_listingResource(resources.ModelResource):
    class Meta:
        model = Room_listing

class Property_listingResource(resources.ModelResource):
    class Meta:
        model = Property_listing

class AgreementResource(resources.ModelResource):
    class Meta:
        model = Agreement

class Agreement_RequestResource(resources.ModelResource):
    class Meta:
        model = Agreement_Request

class InvoiceResource(resources.ModelResource):
    class Meta:
        model = Invoice

class Invoice_LineResource(resources.ModelResource):
    class Meta:
        model = Invoice_Line

class ChatResource(resources.ModelResource):
    class Meta:
        model = Chat

class MessageResource(resources.ModelResource):
    class Meta:
        model = Message

class Payment_WarningResource(resources.ModelResource):
    class Meta:
        model = Payment_Warning

class IncidenceResource(resources.ModelResource):
    class Meta:
        model = Payment_Warning

class CauseResource(resources.ModelResource):
    class Meta:
        model = Cause
