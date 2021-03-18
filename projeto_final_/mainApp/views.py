from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from .models import *
from .forms import *
from django.conf import settings 
from django.core.mail import send_mail
from verify_email.email_handler import send_verification_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.db import connection
from decouple import config
from geopy.geocoders import MapBox
from copy import deepcopy
import PIL
import time
import json
import math
#tirar debug_mode no fim do proj
#tirar test_mode do paypal no fim

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            request.session['popUp'] =  False
            return redirect('index') #placeholder, alterem depois
        else:
            messages.info(request, 'Username ou password incorretos')

            context = {}
            return render(request, 'mainApp/login.html', context) #placeholder
    context = {}
    return render(request,'mainApp/login.html', context) #placeholder

@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('login_view')


def register_view(request):

    if request.user.is_authenticated:
        return redirect('index')

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        pform = ProfileForm(request.POST)

        if form.is_valid() and pform.is_valid():
            inactive_user = send_verification_email(request, form)
            #user = form.save()
            app_user_object = App_user.objects.get(user_id=inactive_user)
            app_user_object.phoneNumber = pform.cleaned_data['phoneNumber']
            app_user_object.birthDate = pform.cleaned_data['birthDate']
            app_user_object.save()

            if request.POST['tipo'] == 'Inquilino':
                ten = Tenant(ten_user=app_user_object)
                ten.save()
            else:
                lord = Landlord(lord_user=app_user_object)
                lord.save()
                
            user_nameStr = form.cleaned_data.get('username')
            user_first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'Utilizador ' + user_nameStr + ' criado!')
            
            request.session['popUp'] =  True
            return redirect('login_view')  

    context = {'form':form, 'errors':form.errors} #, 'pform':pform
    return render(request, 'mainApp/register.html', context)

""" def password_recovery_view(request):
    
    user_id = request.user.id
    subject = "Pedido de mudança de password"
    sender = "noreply.unihouses@gmail.com"
    recipient = form.cleaned_data.get('recovery_email')
    template = "mainApp/templates/mainApp/recovery.html"

    msg = render_to_string(template, raise_exception=True), {"link": verification_url})

    send_mail(subject, strip_tags(msg), from_email=sender, recipient_list=[recipient], html_message=msg) """

def save_property(request):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    prop_content = json.loads(request.session['prop_serial'])
    prop_obj = Property(
        landlord = Landlord.objects.get(lord_user=a_user),
        address = prop_content.get('address'),
        latitude = prop_content.get('latitude'),
        longitude = prop_content.get('longitude'),
        floor_area = prop_content.get('floor_area'),
        garden = prop_content.get('garden'),
        garage = prop_content.get('garage'),
        street_parking = prop_content.get('street_parking'),
        internet = prop_content.get('internet'),
        electricity = prop_content.get('electricity'),
        water = prop_content.get('water'),
        gas = prop_content.get('gas'),
        pets = prop_content.get('pets'),
        overnight_visits = prop_content.get('overnight_visits'),
        cleaning_services = prop_content.get('cleaning_services'),
        smoke = prop_content.get('smoke'),
        bedrooms_num = prop_content.get('bedrooms_num')
    )
    prop_obj.save()

    request.session['prop_id'] = prop_obj.id

    bed_content = json.loads(request.session['bedroom_serial'])
    for c in bed_content:
        bed_obj = Bedroom(
            associated_property = prop_obj,
            be_chairs = c.get('be_chairs'),
            be_sofa = c.get('be_sofa'),
            be_sofa_bed = c.get('be_sofa_bed'),
            be_window = c.get('be_window'),
            num_single_beds = c.get('num_single_beds'),
            num_double_beds = c.get('num_double_beds'),
            be_balcony = c.get('be_balcony'),
            wardrobe = c.get('wardrobe'),
            be_desk = c.get('be_desk'),
            lock = c.get('lock'),
            chest_of_drawers = c.get('chest_of_drawers'),
            tv = c.get('tv'),
            heater = c.get('heater'),
            air_conditioning = c.get('air_conditioning'),
            ensuite_bathroom = c.get('ensuite_bathroom'),
            max_occupacity = c.get('max_occupacity'),
        )
        bed_obj.save()

    bath_content = json.loads(request.session['bathroom_serial'])
    for c in bath_content:
        bath_obj = Bathroom(
            associated_property = prop_obj,
            toilet = c.get('toilet'),
            sink = c.get('sink'),
            shower = c.get('shower'),
            b_window = c.get('b_window'),
            bathtub = c.get('bathtub'),
            bidet = c.get('bidet')
        )
        bath_obj.save()

    kit_content = json.loads(request.session['kitchen_serial'])
    for c in kit_content:
        kit_obj = Kitchen(
            associated_property = prop_obj,
            oven = c.get("oven"),            
            dish_washer = c.get("dish_washer"),  
            k_window = c.get("k_window"),  
            fridge = c.get("fridge"),  
            freezer = c.get("freezer"),  
            cooker = c.get("cooker"),  
            dishes_cutlery = c.get("dishes_cutlery"),  
            pans_pots = c.get("pans_pots"),  
            dishwasher_machine = c.get("dishwasher_machine"),  
            dryer = c.get("dryer"),
            k_table = c.get("k_table"),
            laundering_machine = c.get("laundering_machine"),
            k_chairs = c.get("k_chairs"),
            microwave = c.get("microwave"),
            k_balcony = c.get("k_balcony")
        )
        kit_obj.save()


    if 'livingroom_serial' in request.session:
        liv_content = json.loads(request.session['livingroom_serial'])
        for c in liv_content:
            liv_obj = Livingroom(
                associated_property = prop_obj,
                l_chairs = c.get('l_chairs'),
                l_sofa = c.get('l_sofa'),
                l_sofa_bed = c.get('l_sofa_bed'),
                l_window = c.get('l_window'),
                l_table = c.get('l_table'),
                l_balcony = c.get('l_balcony'),
                l_desk = c.get('l_desk')
            )
            liv_obj.save()

    del request.session['bedroom_serial']
    del request.session['bathroom_serial']
    del request.session['kitchen_serial']
    if 'livingroom_serial' in request.session:
        del request.session['livingroom_serial']
    if 'multiple_bedrooms' in request.session:
        del request.session['multiple_bedrooms']
    
    return redirect('index')

@login_required(login_url='login_view')
def introduce_property_view (request):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('index')

    print(request.session.items())
    if request.user.is_active:

        if request.method == 'POST':

            form_list = []
            bed_form = ''
            bath_form = ''
            kitchen_form = ''
            live_form = ''
            listing_form = ''
            prop_form = ''
            
            if 'bedrooms_num' in request.session.keys():
                bed_form = BedroomFormSet(data=request.POST)
                form_list.append(bed_form)

            elif 'bathrooms_num' in request.session.keys():
                bath_form = BathroomFormSet(data=request.POST)
                form_list.append(bath_form)

            elif 'kitchens_num' in request.session.keys():
                kitchen_form = KitchenFormSet(data=request.POST)
                form_list.append(kitchen_form)

            elif 'livingrooms_num' in request.session.keys():
                live_form = LivingroomFormSet(data=request.POST)
                form_list.append(live_form)

            elif 'listing' in request.session.keys():
                listing_form = ListingForm(request.POST, request.FILES)
                print(request.POST)
                form_list.append(listing_form)
            else:
                prop_form = PropertyForm(data=request.POST)
                form_list.append(prop_form)


            

            for f in form_list:
                if f.is_bound:

                    if f == prop_form:
                        print(f.errors)
                        if f.is_valid():

                            bed_formset = BedroomFormSet(queryset=Bedroom.objects.none())
                            bed_formset.extra = int(f.cleaned_data.get('bedrooms_num'))
                            
                            request.session['bedrooms_num'] =  f.cleaned_data.get('bedrooms_num')
                            request.session['bathrooms_num'] =  f.cleaned_data.get('bathrooms_num')
                            if request.session['bedrooms_num'] > 1:
                                request.session['multiple_bedrooms'] = True

                            request.session['kitchens_num'] =  f.cleaned_data.get('kitchens_num')
                            request.session['livingrooms_num'] =  f.cleaned_data.get('livingrooms_num')
                            if request.session['livingrooms_num'] == 0:
                                request.session['no_living'] = True
                            
                            request.session['l_type'] = f.cleaned_data.get('listing_type')
                            prop_serial = json.dumps(f.cleaned_data)
                            request.session['prop_serial'] = prop_serial

                            context = {
                                'property_form': prop_form,
                                'bed_formset': bed_formset
                                }
                            
                            return render(
                                request,
                                'mainApp/addBedroom.html',
                                context)

                    elif f == bath_form:
                        print(f)
                        bath_serial_list = []
                        for sub_form in f:
                            bath_serial_list.append(sub_form.cleaned_data)

                        bathroom_serial = json.dumps(bath_serial_list)
                        request.session['bathroom_serial'] = bathroom_serial
                        kitchen_formset = KitchenFormSet(queryset=Kitchen.objects.none())

                        kitchen_formset.extra = int(request.session['kitchens_num'])
                        del request.session['bathrooms_num']

                        context = {
                            'kitchen_formset': kitchen_formset}

                        return render(
                            request,
                            'mainApp/addKitchen.html',
                            context)


                    elif f == kitchen_form:
                        print(f)
                        print(request.POST)
                        kit_serial_list = []
                        for sub_form in f:
                            kit_serial_list.append(sub_form.cleaned_data)

                        kitchen_serial = json.dumps(kit_serial_list)
                        request.session['kitchen_serial'] = kitchen_serial

                        if request.session['livingrooms_num'] > 0:
                            live_formset = LivingroomFormSet(queryset=Livingroom.objects.none())

                            live_formset.extra = int(request.session['livingrooms_num'])
                            del request.session['kitchens_num']

                            context = {'live_formset': live_formset}
                            return render(request, 'mainApp/addLivingroom.html', context)

                        elif 'save' in request.POST:
                            save_property(request)

                            del request.session['l_type']
                            del request.session['prop_id']
                            del request.session['kitchens_num']
                            del request.session['livingrooms_num']
                            if 'multiple_bedrooms' in request.session:
                                del request.session['multiple_bedrooms']
                            if 'no_living' in request.session:
                                del request.session['no_living']
                            del request.session['prop_serial']
                            return redirect('index')
                        else:
                            del request.session['kitchens_num']
                            del request.session['livingrooms_num']

                            listing_form = ListingForm()
                            request.session['listing'] =  True
                            save_property(request)
                            imgformset = ImgFormSet(queryset=Image.objects.none())
                            context = {'listing_form': listing_form, 'imgformset' : imgformset}

                            return render(request, 'mainApp/addListing.html', context)


                    elif f == live_form:
                        print(f)
                        liv_serial_list = []
                        for sub_form in f:
                            liv_serial_list.append(sub_form.cleaned_data)

                        livingroom_serial = json.dumps(liv_serial_list)
                        request.session['livingroom_serial'] = livingroom_serial

                        if 'save' in request.POST:
                            save_property(request)

                            del request.session['l_type']
                            del request.session['prop_id']
                            del request.session['livingrooms_num']
                            if 'multiple_bedrooms' in request.session:
                                del request.session['multiple_bedrooms']
                            if 'no_living' in request.session:
                                del request.session['no_living']
                            del request.session['prop_serial']
                            return redirect('index')

                        else:
                            listing_form = ListingForm()
                            save_property(request)
                            request.session['listing'] =  True
                            del request.session['livingrooms_num']

                            imgformset = ImgFormSet(queryset=Image.objects.none())
                            context = {'listing_form': listing_form, 'imgformset' : imgformset}

                            return render(request, 'mainApp/addListing.html', context)
                        
                    
                    elif f == bed_form:
                        print(f)
                        bed_serial_list = []
                        for sub_form in f:
                            bed_serial_list.append(sub_form.cleaned_data)

                        bedroom_serial = json.dumps(bed_serial_list)
                        request.session['bedroom_serial'] = bedroom_serial
                        bath_formset = BathroomFormSet(queryset=Bathroom.objects.none())
                        
                        bath_formset.extra = int(request.session['bathrooms_num'])
                        del request.session['bedrooms_num']

                        context = {'bath_formset': bath_formset}
                        return render(request,'mainApp/addBathroom.html',context)
                        
                    elif 'multiple_listing' in request.POST:
                        del request.session['listing']
                        del request.session['prop_serial']

                        return redirect('propertiesManagement')

                    elif f == listing_form:
                        print(f)
                        if f.is_valid():
                            
                            assoc_prop = Property.objects.get(id=request.session['prop_id'])

                            """ if 'multiple_listing' in f.cleaned_data:
                                if f.cleaned_data.get('multiple_listing') == 'separate':

                                    del request.session['listing']
                                    del request.session['prop_serial']
                                    return redirect('propertiesManagement') """

                            prop_album = ImageAlbum(name=f.cleaned_data.get('title'))
                            prop_album.save()
                            
                            listing_obj = Listing(
                                listing_type = request.session['l_type'],
                                allowed_gender = f.cleaned_data.get('allowed_gender'),
                                monthly_payment =  f.cleaned_data.get('monthly_payment'),
                                availability_starts =  f.cleaned_data.get('availability_starts'),
                                availability_ending =  f.cleaned_data.get('availability_ending'),
                                title =  f.cleaned_data.get('title'),
                                description =  f.cleaned_data.get('description'),
                                security_deposit =  f.cleaned_data.get('security_deposit'),
                                max_capacity =  f.cleaned_data.get('max_capacity'),
                                is_active = True,
                                album = prop_album
                            )
                            listing_obj.save()

                                
                            
                            main_listing = listing_obj
                            del request.session['listing']

                            imgformset = ImgFormSet(request.POST, request.FILES)
                            imgs = imgformset.cleaned_data

                            for d in imgs:
                                cover = False
                                if d == imgs[0]:
                                    cover = True

                                for i in d.values():
                                    if i != None:
                            
                                        img = Image(
                                            name= listing_obj.title+'_'+str(assoc_prop.id),
                                            is_cover = cover,
                                            image = i,
                                            album = prop_album)
                                        img.save()
                                        img_pli = PIL.Image.open(img.image)  
                                        img_r = img_pli.resize((600,337.5))
                                        img_r.save(str(img.image))

                            del request.session['prop_serial']

                            if request.session['l_type'] == 'Apartment' or request.session['l_type'] == 'House':
                                #if f.cleaned_data.get('multiple_listing') == 'whole':
                                apart_obj = Property_listing(main_listing = main_listing, associated_property = assoc_prop)
                                apart_obj.save()
                                return redirect('index')
                                

                            elif request.session['l_type'] == 'Bedroom' or request.session['l_type'] == 'Studio':
                                room_obj = Room_listing(
                                    main_listing = main_listing,
                                    associated_room = Bedroom.objects.get(associated_property = assoc_prop))
                                room_obj.save()
                                
                                return redirect('index')


            return redirect('index')     #PLACEHOLDER
                            
        else:
            prop_form = PropertyForm()
            bath_formset = BathroomFormSet(queryset=Bathroom.objects.none())
            kitchen_formset = KitchenFormSet(queryset=Kitchen.objects.none())
            live_formset = LivingroomFormSet(queryset=Livingroom.objects.none())
            bed_formset = BedroomFormSet(queryset=Bedroom.objects.none())
            listing_form = ListingForm()

            return render(
                request,
                'mainApp/addProperty.html',
                {'property_form': prop_form,
                'bath_formset': bath_formset,
                'kitchen_formset': kitchen_formset,
                'live_formset': live_formset,
                'bed_formset': bed_formset,
                'listing_form': listing_form
                })
    else:
        return redirect('index')

#@login_required(login_url='login_view')
def index(request):
    return render(request, "mainApp/home.html", {})

@login_required(login_url='login_view')
def accept_request(request, request_id):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    print('pls_get_in')
    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('search')

    ag_request = Agreement_Request.objects.get(id=request_id)
    ag_request.accepted = True
    ag_request.save()

    return redirect('profile')

@login_required(login_url='login_view')
def deny_request(request, request_id):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    print('pls_DONT_get_in')
    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('search')

    ag_request = Agreement_Request.objects.get(id=request_id)
    ag_request.accepted = False
    ag_request.save()

    return redirect('profile')


def create_agreement(user_id, ag_request_id):

    current_user = User.objects.get(id=user_id)
    a_user = App_user.objects.get(user_id=current_user)

    try:
        tenant = Tenant.objects.get(ten_user=a_user)
    except:
        return redirect('search')


    request_id = ag_request_id
    ag_request = Agreement_Request.objects.get(id= request_id)
    assoc_listing = ''
    new_ag = ''

    if ag_request.associated_property_listing:
        assoc_listing = ag_request.associated_property_listing
        lord = assoc_listing.associated_property.landlord

        new_ag = Agreement(
            associated_property_listing = assoc_listing,
            tenant = tenant,
            landlord = lord,
            startsDate = ag_request.startsDate,
            endDate= ag_request.endDate
        )
        new_ag.save()
        assoc_listing.main_listing.is_active = False
        assoc_listing.save()

    else:
        assoc_listing = ag_request.associated_room_listing
        lord = assoc_listing.associated_room.associated_property.landlord

        new_ag = Agreement(
            associated_room_listing = assoc_listing,
            tenant = tenant,
            landlord = lord,
            startsDate = ag_request.startsDate,
            endDate= ag_request.endDate
        )
        new_ag.save()
        assoc_listing.main_listing.is_active = False
        assoc_listing.save()
        

@login_required(login_url='login_view')
def create_request(request):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    try:
        ten = Tenant.objects.get(ten_user=a_user)
    except:
        return redirect('search')

    if request.method == 'POST':

        ag_form = Agreement_Request_Form(data=request.POST)

        if ag_form.is_valid():
            room_id = request.session.get('room_listing')
            prop_id = request.session.get('property_listing')
            tenant_id = request.session.get('tenant')
            landlord_id = request.session.get('landlord')
            start_date = ag_form.cleaned_data.get('startsDate')
            end_date = ag_form.cleaned_data.get('endDate')
            message = ag_form.cleaned_data.get('message')

            if 'room_listing' in request.session:
                del request.session['room_listing']
                del request.session['tenant']
                del request.session['landlord']
            elif 'property_listing' in request.session:
                del request.session['property_listing']
                del request.session['tenant']
                del request.session['landlord']

            if room_id:
                
                assoc_listing = Room_listing.objects.get(id=room_id)
                tenant = Tenant.objects.get(id=tenant_id)
                landlord = Landlord.objects.get(id=landlord_id)

                ag_request = Agreement_Request(
                    associated_room_listing = assoc_listing,
                    tenant=tenant,
                    landlord=landlord,
                    startsDate=start_date,
                    endDate=end_date,
                    message=message
                )
                ag_request.save()

                return redirect('index')

            else:
                assoc_listing = Property_listing.objects.get(id=prop_id)
                tenant = Tenant.objects.get(id=tenant_id)
                landlord = Landlord.objects.get(id=landlord_id)

                ag_request = Agreement_Request(
                    associated_property_listing = assoc_listing,
                    tenant=tenant,
                    landlord=landlord,
                    startsDate=start_date,
                    endDate=end_date,
                    message=message
                )
                ag_request.save()

                return redirect('index')

    else:
        return render(request, 'mainApp/intent.html')

@login_required(login_url='login_view')
def profile(request):
    return render(request, "mainApp/profile.html", {})

def properties_management_view(request):
    current_user = request.user
    app_user = App_user.objects.get(user_id = current_user)
    a_user = Landlord.objects.get(lord_user_id=app_user)
    properties = list(Property.objects.filter(landlord_id = a_user))

    context = {"properties":properties}
    return render(request, "mainApp/propertiesManagement.html", context)

def property_editing_view(request, property_id=None):
    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('index')

    property_object = Property.objects.get(id=property_id)
    

    if request.method == 'POST':
        f = UpdatePropertyForm(request.POST, instance=property_object)
        
        if f.is_valid():
            f.save() 
           
        return redirect("/mainApp/profile/propertiesManagement/bedroomsEditing/{}".format(property_object.id))    
    context={"property":property_object}
    return render(request, "mainApp/editProperty.html", context)

def bedrooms_editing_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    bedrooms_queryset = Bedroom.objects.filter(associated_property=property_object)
    bedrooms_list = list(bedrooms_queryset)
    bedrooms_listing = []
    for bedroom in bedrooms_list:
        try:
            room_listing = Room_listing.objects.get(associated_room=bedroom)
            bedrooms_listing.append(True)
        except:
            bedrooms_listing.append(False)
    if request.method == 'POST':
        bed_formset = BedroomFormSet(request.POST, queryset=bedrooms_queryset)
        if bed_formset.is_valid():
            for form in bed_formset.forms:
                bedroom = form.save(commit="False")
                bedroom.associated_property = property_object
                bedroom.save()

            return redirect("/mainApp/profile/propertiesManagement/bathroomsEditing/{}".format(property_object.id))    
    else:        
        bed_formset = BedroomFormSet(queryset=bedrooms_queryset)
        bed_formset.extra=0
    
    forms = [form for form in bed_formset]
    bedrooms_info_zip = zip(forms, bedrooms_listing)
    context = {'bed_formset':bed_formset, 'property_id':property_id, 'bedrooms_info_zip':bedrooms_info_zip}
    return render(request, "mainApp/editBedrooms.html", context)

def bedroom_delete_view(request, bedroom_id, property_id):
    bedroom_object = Bedroom.objects.get(id=bedroom_id)
    try:
        room_listing = Room_listing.objects.get(associated_room=bedroom_object)
    except:
        room_listing = None

    if room_listing == None:
        bedroom_object.delete()
    else:
        request.session['bedroom_delete_error'] = True
    
    return redirect("/mainApp/profile/propertiesManagement/bedroomsEditing/{}".format(property_id))

def bathrooms_editing_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    bathrooms_queryset = Bathroom.objects.filter(associated_property=property_object)
    if request.method == 'POST':
        bath_formset = BathroomFormSet(request.POST, queryset=bathrooms_queryset)
        if bath_formset.is_valid():
            for form in bath_formset.forms:
                form.save()      
            return redirect("/mainApp/profile/propertiesManagement/kitchensEditing/{}".format(property_object.id)) 
    else:        
        bath_formset = BathroomFormSet(queryset=bathrooms_queryset)
        bath_formset.extra=0

    context = {'bath_formset':bath_formset}
    return render(request, "mainApp/editBathrooms.html", context)

def kitchens_editing_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    kitchens_queryset = Kitchen.objects.filter(associated_property=property_object)
    if request.method == 'POST':
        kitchen_formset = KitchenFormSet(request.POST, queryset=kitchens_queryset)
        if kitchen_formset.is_valid():
            for form in kitchen_formset.forms:
                form.save()    
            return redirect("/mainApp/profile/propertiesManagement/livingroomsEditing/{}".format(property_object.id))
    else:        
        kitchen_formset = KitchenFormSet(queryset=kitchens_queryset)
        kitchen_formset.extra=0

    context = {'kitchen_formset':kitchen_formset}
    return render(request, "mainApp/editKitchens.html", context)

def livingrooms_editing_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    livingrooms_queryset = Livingroom.objects.filter(associated_property=property_object)
    if request.method == 'POST':
        livingroom_formset = LivingroomFormSet(request.POST, queryset=livingrooms_queryset)
        if livingroom_formset.is_valid():
            for form in livingroom_formset.forms:
                form.save()    
            #return redirect("/mainApp/profile/propertiesManagement/livingroomsEditing/{}".format(property_object.id))
    else:        
        livingroom_formset = LivingroomFormSet(queryset=livingrooms_queryset)
        livingroom_formset.extra=0

    context = {'live_formset':livingroom_formset}
    return render(request, "mainApp/editLivingrooms.html", context)

def listing_editing_view(request, property_id):
    return render(request, "mainApp/listingEdit.html", {})


def notificationsTenant(request):
    current_user_ = request.user
    a_user_ = App_user.objects.get(user_id=current_user_)

    try:
        tenant_ = Tenant.objects.get(ten_user=a_user_)
    except:
        return redirect('profile')

    listOfAgreements = []
    for e in Agreement_Request.objects.all():
        if e.tenant_id == tenant_.id:
            listOfAgreements.append(e)
    print("LISTA DOS AGREEMENTS DESTE USER: ", listOfAgreements)
    fullList = []
    for a in listOfAgreements:
        _id_req = a.id
        _landlord_ = a.landlord #objeto landlord
        _userLand_ = _landlord_.lord_user
        userLand = _userLand_.user
        nomeLand = userLand.username
        message = a.message 
        startsDate = a.startsDate
        endDate = a.endDate
        accepted = a.accepted #para ver se esta null, aceite ou recusada
        fullList.append([_id_req, nomeLand, message, startsDate, endDate, accepted])
    sizeList = len(fullList)
    #print(fullList)
    #ola = Agreement_Request.objects.get(landlord_id=1)
    #print(ola.tenant_id)
    context = {"fullList" : fullList, "sizeList": sizeList}
    return render(request, "mainApp/notificationsTenant.html", context)

def notificationsLandlord(request):
    current_user_ = request.user
    a_user_ = App_user.objects.get(user_id=current_user_)

    try:
        landlord_ = Landlord.objects.get(lord_user=a_user_)
    except:
        return redirect('profile')

    listOfAgreements_ = []
    for e in Agreement_Request.objects.all():
        if e.landlord_id == landlord_.id:
            listOfAgreements_.append(e)
    print("LISTA DOS AGREEMENTS DESTE LANDLORD: ", listOfAgreements_)
    fullList_ = []
    for a in listOfAgreements_:
        id_req = a.id
        user_ = a.tenant #objeto tenant
        _user_ = user_.ten_user
        userTen = _user_.user
        nomeTen = userTen.username
        message_ = a.message 
        startsDate_ = a.startsDate
        endDate_ = a.endDate
        accepted_ = a.accepted #vem sempre a null, pronta a ser definida pelo landlord
        fullList_.append([id_req, nomeTen, message_, startsDate_, endDate_, accepted_])
    sizeList = len(fullList_)
    #ola = Agreement_Request.objects.get(landlord_id=1)
    #print(ola.tenant_id)
    context = {"fullList_": fullList_, 'range': range(sizeList)}
    return render(request, "mainApp/notificationsLandlord.html", context)

""" def accReq(request, id_Req):
    #UserProfile.objects.filter(user=request.user).update(level='R')
    Agreement_Request.objects.filter(id=id_Req).update(accepted='True')
    #for e in Agreement_Request.objects.all():
       # if e.id == id_Req:
         #   e.update(accepted='True')
    return render(request, "mainApp/notificationsLandlord.html", {})


def denReq(request, id_Req):
    Agreement_Request.objects.filter(id=id_Req).update(accepted='False')
    #for e in Agreement_Request.objects.all():
        #if e.id == id_Req:
          #  e.update(accepted='False')
    return render(request, "mainApp/notificationsLandlord.html", {}) """

def get_distance(lat_1, lng_1, lat_2, lng_2): 
    d_lat = lat_2 - lat_1
    d_lng = lng_2 - lng_1 

    temp = (  
         math.sin(d_lat / 2) ** 2 
       + math.cos(lat_1) 
       * math.cos(lat_2) 
       * math.sin(d_lng / 2) ** 2
    )

    return 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))

def search(request):
    form = CreateUserForm()
    geolocator = MapBox(config('MAPBOX_KEY'), scheme=None, user_agent=None, domain='api.mapbox.com')
    location = ''
    row = ''
    searched = False

    searched_values = []
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():

            searched = True
            location = geolocator.geocode(form.cleaned_data.get('location'))
            searched_values.extend((location.latitude, location.longitude, form.cleaned_data.get('radius')))
            querySelect = 'SELECT l.monthly_payment, l.title, p.address, p.latitude, p.longitude, i.image'
            queryFrom = ' FROM mainApp_listing AS l, mainApp_property as p, mainApp_image as i'
            queryWhere = " WHERE (acos(sin(p.latitude * 0.0175) * sin("+str(location.latitude)+"* 0.0175) \
                            + cos(p.latitude * 0.0175) * cos("+str(location.latitude)+" * 0.0175) *    \
                                cos(("+str(location.longitude)+" * 0.0175) - (p.longitude * 0.0175))\
                            ) * 6371 <='" + str(form.cleaned_data.get('radius')) + "')"

            cursor = connection.cursor()
            
            queryWhere += " AND l.album_id = i.album_id AND i.is_cover = 1"

            #Checks if the price is within range
            if (form.cleaned_data.get('maxPrice') == '2000'):
                queryWhere += " AND  l.monthly_payment >= '" + form.cleaned_data.get('minPrice') + "'"
            else:
                queryWhere += " AND l.monthly_payment BETWEEN '" + form.cleaned_data.get('minPrice') + "' AND '"\
                                + form.cleaned_data.get('maxPrice') + "' AND l.album_id = i.album_id AND i.is_cover = 1"

            #Number of tenants is filled
            if any(form.cleaned_data.get('num_tenants') == x for x in ('1','2','3','4')):
                queryWhere += " AND l.max_capacity = '" + form.cleaned_data.get('num_tenants') + "'"
            elif(form.cleaned_data.get('num_tenants') == '5'):
                queryWhere += " AND l.max_capacity >= 5"

            #Date in is filled
            if form.cleaned_data.get('date_in') is not None:
                queryWhere += " AND '" + str(form.cleaned_data.get('date_in')) + "' >= l.availability_starts"
            
            #Date out is filled
            if form.cleaned_data.get('date_out') is not None:
                queryWhere += " AND '" + str(form.cleaned_data.get('date_out')) + "' <= l.availability_ending"

            #Number of bedrooms is filled
            print(form.cleaned_data.get('num_bedrooms'))
            if any(form.cleaned_data.get('num_bedrooms') == x for x in ('1','2','3','4')):
                queryWhere += " AND p.bedrooms_num = '" + form.cleaned_data.get('num_bedrooms') + "'"
            elif(form.cleaned_data.get('num_bedrooms') == '5'):
                queryWhere += " AND p.bedrooms_num >= 5"
            
            #Property type is filled and is either Bedroom, Studio or Residency
            if any( form.cleaned_data.get('type') == x for x in ('Bedroom', 'Studio', 'Residency')):
                queryFrom += ', mainApp_room_listing AS rl'
                queryWhere += " AND l.listing_type = '" + form.cleaned_data.get('type') + "'\
                                AND rl.associated_room_id = p.id AND rl.main_listing_id = l.id"
                #print(querySelect + queryFrom + queryWhere)
                cursor.execute(querySelect + queryFrom + queryWhere)
                row = cursor.fetchall()

            #Property type is filled and is either Apartment or House
            elif any( form.cleaned_data.get('type') == x for x in ('Apartment', 'House')):
                queryFrom += ', mainApp_property_listing AS pl'
                queryWhere += " AND l.listing_type = '" + form.cleaned_data.get('type') + "'\
                                AND pl.associated_property_id = p.id AND pl.main_listing_id = l.id"
                #print(querySelect + queryFrom + queryWhere)
                cursor.execute(querySelect + queryFrom + queryWhere)
                row = cursor.fetchall()
            
            #Property type is empty
            else:         
                queryFromProperty = deepcopy(queryFrom) + ', mainApp_property_listing AS pl'
                queryWhereProperty = deepcopy(queryWhere) + ' AND pl.associated_property_id = p.id AND pl.main_listing_id = l.id'

                queryFromRoom = deepcopy(queryFrom) + ', mainApp_room_listing AS rl'
                queryWhereRoom = deepcopy(queryWhere) + ' AND rl.associated_room_id = p.id AND rl.main_listing_id = l.id'

                cursor.execute(querySelect + queryFromProperty + queryWhereProperty)
                row_property = cursor.fetchall()

                cursor.execute(querySelect + queryFromRoom+ queryWhereRoom)
                row_room = cursor.fetchall()

                row = row_property + row_room

    for i in range(len(row)):
        lng_1, lat_1, lng_2, lat_2 = map(math.radians, [location.longitude, location.latitude, row[i][4], row[i][3]])
        print(row[i][5])
        tempTuple = row[i][:5] + (row[i][5].split('mainApp/static/')[1],) + row[i][6:] + (round(get_distance(lng_1, lat_1, lng_2, lat_2),1),)
        row = row[:i] + (tempTuple,) + row[i+1:]

    context = {
        'searched_values' : searched_values,  #list with 3 elements containing the coordinates of the searched address and radius of the search 
        'num_results' : len(row), 
        'row' : row,
        'searched' : searched,
    }
    return render(request, "mainApp/search.html", context)


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    images = Image.objects.filter(album_id=listing.album_id)
    listing_type = listing.listing_type
    bedrooms = []

    if 'room_listing' in request.session:
        del request.session['room_listing']
        del request.session['tenant']
        del request.session['landlord']
    elif 'property_listing' in request.session:
        del request.session['property_listing']
        del request.session['tenant']
        del request.session['landlord']

    if listing_type == "Bedroom" or listing_type == "Residency" or listing_type == "Studio":
        associated_object = listing.r_main.associated_room #associated object is a Bedroom
        parent_property = associated_object.associated_property
        bedrooms.append(associated_object)

        request.session['room_listing'] = Room_listing.objects.get(associated_room=associated_object).id
    

    else:
        associated_object = listing.p_main.associated_property #associated object is a property
        parent_property = associated_object

        bedrooms = list(Bedroom.objects.filter(associated_property = parent_property))

        request.session['property_listing'] = Property_listing.objects.get(associated_property=associated_object).id
        
    num_beds = 0
    for bedroom in bedrooms:
        num_beds += (bedroom.num_double_beds + bedroom.num_single_beds)
    
    bathrooms = list(Bathroom.objects.filter(associated_property = parent_property))
    kitchens = list(Kitchen.objects.filter(associated_property = parent_property))
    livingrooms = list(Livingroom.objects.filter(associated_property = parent_property))
    landlord = parent_property.landlord
    landlord_user = landlord.lord_user.user
    rooms_count_details = [bathrooms, bedrooms, kitchens, livingrooms, [parent_property]]
    num_details = 0

    for room in rooms_count_details:
        num_details += countRoomDetails(room)

    if request.user.is_authenticated:
        app_user = App_user.objects.get(user=request.user)
        print(app_user)
        is_tenant = True
        try:
            tenant = Tenant.objects.get(ten_user=app_user)
            request.session['tenant'] = tenant.id
            request.session['landlord'] = landlord.id
        except:
            is_tenant = False
            messages.info(request, 'Opção reservada a inquilinos.', extra_tags='tenant_lock')
            request.session['tenant'] = None
            request.session['landlord'] = None
    else:
        is_tenant = True
        request.session['tenant'] = None
        request.session['landlord'] = None

    #print(list(images)[0].image)
    imagesPaths = []
    range = [0,]
    for i in list(images):
        pathSplited = str(i.image).split('mainApp/static/')
        imagesPaths.append(pathSplited[1])
        range.append(int(range[-1]) + 1)

    context  = {
        "listing": listing,
        "landlord_user": landlord_user,
        "bedrooms": bedrooms,
        "num_beds": num_beds,
        "bathrooms": bathrooms,
        "property": parent_property,
        "kitchens": kitchens,
        "numDetails": num_details,
        "livingrooms": livingrooms,
        "security_deposit": listing.security_deposit,
        "is_tenant": is_tenant,
        "imagesPaths": imagesPaths,
        "range": range[:-1],
        "zipPaths": zip(imagesPaths, range[:-1]),
    }
    return render(request, "mainApp/listingPage.html", context)

def countRoomDetails(rooms):
     
    num_details = 0
    for room in rooms:
        for k, v in model_to_dict(room).items():
            if v == True and isinstance(v, bool):
                num_details+=1
    
    return num_details

@login_required(login_url='login_view')
def make_payment(request, ag_request_id):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    try:
        tenant = Tenant.objects.get(ten_user=a_user)
    except:
        return redirect('search')

    if request.method == 'POST':

        ag_request = Agreement_Request.objects.get(id=ag_request_id)
        if ag_request.tenant == tenant and ag_request.accepted == True:

            if ag_request.associated_property_listing == None:
                room_listing = ag_request.associated_room_listing
                assoc_room = room_listing.associated_room
                assoc_prop = assoc_room.associated_property
                lord = assoc_prop.landlord
                main_listing = room_listing.main_listing

            else:
                prop_listing = ag_request.associated_property_listing
                assoc_prop = prop_listing.associated_property
                lord = assoc_prop.landlord
                main_listing = property_listing.main_listing

            lord_receiver_email = lord.lord_user.user.email
            duration_days = (ag_request.endDate - ag_request.startsDate).days
            total_amount = int((duration_days/30) * main_listing.monthly_payment)

            paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": total_amount,
            "currency_code": "EUR",
            "no_note": "1",
            "item_name": main_listing.title,
            "item_number": ag_request.id,
            "custom": current_user.id,
            "notify_url": "http://179c45eda6a9.ngrok.io/paymentStatus/",
            "return_url": "http://179c45eda6a9.ngrok.io/mainApp/search",
            "cancel_return": "http://179c45eda6a9.ngrok.io/mainApp/search",

            }
            payment_form = PayPalPaymentsForm(initial=paypal_dict)
            context = {'pp_form':payment_form}

            return render(request, template_name='mainApp/payment.html', context=context)
        
        else:
            return redirect('search')

@csrf_exempt
def get_payment_status(sender, **kwargs):
    
    ipn_obj = sender.POST
    if ipn_obj['payment_status'] == ST_PP_COMPLETED:

        if ipn_obj['receiver_email'] == settings.PAYPAL_RECEIVER_EMAIL:

            ag_request_id = ipn_obj['item_number']
            user_id = ipn_obj['custom']
            create_agreement(user_id, ag_request_id)

    return redirect('index')

valid_ipn_received.connect(get_payment_status)
invalid_ipn_received.connect(get_payment_status)

def changeToRegister(request):
    return render(request, "mainApp/register.html", {})
