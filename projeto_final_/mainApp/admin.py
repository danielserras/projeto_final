from django.contrib import admin
from django.contrib.auth.models import User
from mainApp.models import *
from import_export.admin import ImportExportModelAdmin
import mainApp
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.apps import apps
from mainApp.resources import *
import inspect
import sys

models = apps.get_models()
filteredModels = []




class UserAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_class = UserResource

class App_userAdmin(ImportExportModelAdmin):
    resource_class = AppUserResource

class TenantAdmin(ImportExportModelAdmin):
    resource_class = TenantResource

class LandlordAdmin(ImportExportModelAdmin):
    resource_class = LandlordResource

class ImageAlbumAdmin(ImportExportModelAdmin):
    resource_class = ImageAlbumResource

class ImageAdmin(ImportExportModelAdmin):
    resource_class = ImageResource

class PropertyAdmin(ImportExportModelAdmin):
    resource_class = PropertyResource

class BathroomAdmin(ImportExportModelAdmin):
    resource_class = BathroomResource

class KitchenAdmin(ImportExportModelAdmin):
    resource_class = KitchenResource

class LivingroomAdmin(ImportExportModelAdmin):
    resource_class = LivingroomResource

class ListingAdmin(ImportExportModelAdmin):
    resource_class = ListingResource

class Room_listingAdmin(ImportExportModelAdmin):
    resource_class = Room_listingResource

class Property_listingAdmin(ImportExportModelAdmin):
    resource_class = Property_listingResource

class AgreementAdmin(ImportExportModelAdmin):
    resource_class = AgreementResource

class Agreement_RequestAdmin(ImportExportModelAdmin):
    resource_class = Agreement_RequestResource

class InvoiceAdmin(ImportExportModelAdmin):
    resource_class = InvoiceResource

class Invoice_LineAdmin(ImportExportModelAdmin):
    resource_class = Invoice_LineResource

class ChatAdmin(ImportExportModelAdmin):
    resource_class = ChatResource

class MessageAdmin(ImportExportModelAdmin):
    resource_class = MessageResource

class Payment_WarningAdmin(ImportExportModelAdmin):
    resource_class = Payment_WarningResource

class IncidenceAdmin(ImportExportModelAdmin):
    resource_class = IncidenceResource

class CauseAdmin(ImportExportModelAdmin):
    resource_class = CauseResource

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(App_user, App_userAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Landlord, LandlordAdmin)
admin.site.register(ImageAlbum, ImageAlbumAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Bathroom, BathroomAdmin)
admin.site.register(Kitchen, KitchenAdmin)
admin.site.register(Livingroom, LivingroomAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Room_listing, Room_listingAdmin)
admin.site.register(Property_listing, Property_listingAdmin)
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(Agreement_Request, Agreement_RequestAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Invoice_Line, Invoice_LineAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Payment_Warning, Payment_WarningAdmin)
admin.site.register(Cause, CauseAdmin)
admin.site.register(Incidence, IncidenceAdmin)


""" for model in models:
    if model._meta.app_label == "mainApp":
        filteredModels.append(model)

classList = inspect.getmembers(sys.modules[__name__], inspect.isclass)
filteredClassList = []
for class_0 in classList:
    if (class_0[0]).endswith("Admin"):
        filteredClassList.append(class_0)
print(filteredClassList) """



