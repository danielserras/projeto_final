from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
import time

def get_upload_path(instance, filename):
    path = instance.album.ListingAlbum.id
    return f'mainApp/static/mainApp/listings/{path}/{filename}'


class App_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField(null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)

class Tenant(models.Model):
    ten_user = models.OneToOneField(App_user, on_delete=models.CASCADE)
    university = models.CharField(max_length=100, null=True, blank=True)
    min_search = models.IntegerField(default=500)
    max_search = models.IntegerField(default=1200)

class Landlord(models.Model):
    lord_user = models.OneToOneField(App_user, on_delete=models.CASCADE)
    lord_type = models.CharField(max_length=30, default='Particular')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        App_user.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.app_user.save()


class ImageAlbum(models.Model):
    name = models.CharField(max_length=250)


class Image(models.Model):
    name = models.CharField(max_length=250)
    is_cover = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_upload_path)
    album = models.ForeignKey(ImageAlbum, related_name="images", on_delete=models.CASCADE)


class Property(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    floor_area = models.IntegerField()              
    garden = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)
    street_parking = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    electricity = models.BooleanField(default=False)             
    water = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    overnight_visits = models.BooleanField(default=False)
    cleaning_services = models.BooleanField(default=False)
    smoke = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=20, decimal_places=14)
    longitude = models.DecimalField(max_digits=20, decimal_places=14)
    bedrooms_num = models.IntegerField()
    listing_type = models.CharField(max_length=20)
    


class Bathroom(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE, related_name = "bathroom", null=True, blank=True)
    toilet = models.BooleanField() 
    sink = models.BooleanField()
    shower = models.BooleanField()
    b_window = models.BooleanField()
    bathtub = models.BooleanField()
    bidet = models.BooleanField()

class Bedroom(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE, related_name="bedroom", null=True, blank=True)
    be_chairs = models.BooleanField()
    be_sofa = models.BooleanField()
    be_sofa_bed = models.BooleanField()
    be_window = models.BooleanField()
    num_single_beds = models.IntegerField()
    num_double_beds = models.IntegerField()
    max_occupancy = models.IntegerField()
    be_balcony = models.BooleanField()
    wardrobe = models.BooleanField()
    be_desk = models.BooleanField()
    chest_of_drawers = models.BooleanField()
    tv = models.BooleanField()
    heater = models.BooleanField()
    air_conditioning = models.BooleanField()
    lock = models.BooleanField()
    ensuite_bathroom = models.BooleanField()

class Kitchen(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE, related_name="kitchen", null=True, blank=True)
    dish_washer = models.BooleanField()
    k_window = models.BooleanField()
    fridge = models.BooleanField()
    freezer = models.BooleanField()
    cooker = models.BooleanField()
    dishes_cutlery = models.BooleanField()
    pans_pots = models.BooleanField()
    dishwasher_machine = models.BooleanField()
    dryer = models.BooleanField() 
    oven = models.BooleanField()
    k_table = models.BooleanField()
    laundering_machine = models.BooleanField()
    k_chairs = models.BooleanField()
    microwave = models.BooleanField()
    k_balcony = models.BooleanField()



class Livingroom(models.Model):
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE, related_name="livingroom", null=True, blank=True)
    l_chairs = models.BooleanField()
    l_sofa = models.BooleanField()
    l_sofa_bed = models.BooleanField()
    l_window = models.BooleanField()
    l_table = models.BooleanField()
    l_balcony = models.BooleanField()
    l_desk = models.BooleanField()

class Listing(models.Model):
    allowed_gender = models.CharField(max_length=20)
    monthly_payment = models.IntegerField()
    availability_starts = models.DateField()
    availability_ending = models.DateField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=280)
    security_deposit = models.IntegerField()
    max_occupancy = models.IntegerField()
    listing_type = models.CharField(max_length=20)
    is_active = models.BooleanField()
    album = models.OneToOneField(ImageAlbum, related_name="ListingAlbum", on_delete=models.CASCADE, blank=True, null=True)



class Room_listing(models.Model):
    main_listing = models.OneToOneField(Listing, on_delete = models.CASCADE, related_name='r_main')
    associated_room = models.ForeignKey(Bedroom, on_delete = models.CASCADE)

class Property_listing(models.Model):
    main_listing = models.OneToOneField(Listing, on_delete = models.CASCADE, related_name='p_main')
    associated_property = models.ForeignKey(Property, on_delete = models.CASCADE)

class Agreement(models.Model):
    associated_room_listing = models.ForeignKey(Room_listing, models.SET_NULL, null=True)
    associated_property_listing = models.ForeignKey(Property_listing, models.SET_NULL, null=True)
    tenant = models.ForeignKey(Tenant, models.SET_NULL, null=True)
    landlord = models.ForeignKey(Landlord, models.SET_NULL, null=True)
    startsDate = models.DateField()
    endDate = models.DateField()
    last_invoice_date = models.DateField()
    status = models.BooleanField()


class Rich_Text_Message(models.Model):
    message = RichTextField(null=True, blank=True)

class Agreement_Request(models.Model):
    associated_room_listing = models.ForeignKey(Room_listing, models.SET_NULL, null=True)
    associated_property_listing = models.ForeignKey(Property_listing, models.SET_NULL, null=True)
    tenant = models.ForeignKey(Tenant, models.SET_NULL, null=True)
    landlord = models.ForeignKey(Landlord, models.SET_NULL, null=True)
    startsDate = models.DateField()
    endDate = models.DateField()
    message = models.TextField(null=True, blank=True)
    messageLandlord =  models.ForeignKey(Rich_Text_Message, models.SET_NULL, null=True)
    accepted = models.BooleanField(null=True, blank=True)
    dateOfRequest = models.DateTimeField()
    checkReadLandlord = models.BooleanField()
    checkReadTenant = models.BooleanField()

class Invoice(models.Model):
    agreement_request = models.ForeignKey(Agreement_Request, null=True, on_delete=models.CASCADE)
    agreement = models.ForeignKey(Agreement, null=True, on_delete=models.CASCADE)
    timestamp = models.DateField()
    month = models.DateField(null=True)
    paid = models.BooleanField()
    checkReadTenant = models.BooleanField()

class Invoice_Line(models.Model):
    description = models.CharField(max_length=280)
    amount = models.IntegerField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

class Payment_Warning(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    checkReadTenant = models.BooleanField()

class Refund(models.Model):
    value = models.FloatField()
    tenant = models.ForeignKey(Tenant, models.SET_NULL, null=True)
    landlord = models.ForeignKey(Landlord, models.SET_NULL, null=True)
    agreement = models.ForeignKey(Agreement, models.SET_NULL, null=True)
    status = models.BooleanField()
    checkReadLandlord = models.BooleanField()
    dateOfRequest = models.DateTimeField()
    
class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

class Chat(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_1")
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_2")
    last_message = models.DateTimeField()

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField()
    is_read = models.BooleanField()

    def as_json(self):
        return dict(
            message_id = self.id,
            chat = self.chat.id,
            sender = self.sender.username,
            content = self.content,
            timestamp = self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            is_read = self.is_read
        )

class Cause(models.Model):
    description = models.CharField(max_length=100)


class Incidence(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    filing_time = models.DateField()
    causes = models.ManyToManyField(Cause)
    description = models.CharField(max_length=280)
    grouds_for_termination = models.BooleanField(null=True)
