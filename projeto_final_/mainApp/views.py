from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from .models import *
from .forms import *
from .utils import render_to_pdf
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
from django.template.loader import get_template
from django.db import connection
from decouple import config
from geopy.geocoders import MapBox
from copy import deepcopy
from django.utils import translation
from django.utils.translation import gettext as _
from datetime import datetime, timedelta, date
from django.views.generic import View
import PIL
import time
import json
import math
import os
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
            a_user = user.username
            id_user = user.id
            for i in Landlord.objects.all():
                if i.lord_user_id == id_user:
                    request.session['typeUser'] = "Landlord"
                    return redirect('index') #placeholder, alterem depois
            for i in Tenant.objects.all():
                if i.ten_user_id == id_user:
                    request.session['typeUser'] = "Tenant"
                    return redirect('index') #placeholder, alterem depois
        else:
            mistakes = 'Nome de utilizador ou palavra-passe incorretos'
            context = {'mistakes': mistakes}
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
    pform = ProfileForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        pform = ProfileForm(request.POST)

        #para verificar email ver https://github.com/foo290/Django-Verify-Email/   -alexfaustino
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
            #messages.success(request, _('Utilizador ') + user_nameStr + _(' criado!'))
            
            request.session['popUp'] =  True
            return redirect('login_view')  

    context = {'form':form, 'pform': pform, 'errors':form.errors} #, 'pform':pform
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
        bedrooms_num = prop_content.get('bedrooms_num'),
        listing_type = request.session["l_type"]
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
            max_occupancy = c.get('max_occupancy'),
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
                try:
                    del request.session['bedroom_serial']
                except:
                    pass
                bed_form = BedroomFormSet(data=request.POST)
                form_list.append(bed_form)

            elif 'bathrooms_num' in request.session.keys():
                try:
                    del request.session['bathroom_serial']
                except:
                    pass
                bath_form = BathroomFormSet(data=request.POST)
                form_list.append(bath_form)

            elif 'kitchens_num' in request.session.keys():
                try:
                    del request.session['kitchen_serial']
                except:
                    pass
                kitchen_form = KitchenFormSet(data=request.POST)
                form_list.append(kitchen_form)

            elif 'listing' in request.session.keys():
                listing_form = ListingForm(request.POST, request.FILES)
                form_list.append(listing_form)

            elif 'livingrooms_num' in request.session.keys():
                try:
                    del request.session['livingroom_serial']
                except:
                    pass
                live_form = LivingroomFormSet(data=request.POST)
                form_list.append(live_form)

            else:
                try:
                    del request.session['prop_serial']
                except:
                    pass
                prop_form = PropertyForm(data=request.POST)
                form_list.append(prop_form)


            current_date = datetime.today().strftime('%Y-%m-%d')

            for f in form_list:
                if f.is_bound:

                    if f == prop_form:
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

                            request.session['addPropPopUp'] =  True
                            return redirect('profile')  #sair
                        else:
                            del request.session['kitchens_num']
                            #del request.session['livingrooms_num']

                            listing_form = ListingForm()
                            request.session['listing'] =  True
                            save_property(request)
                            imgformset = ImgFormSet(queryset=Image.objects.none())
                            context = {'listing_form': listing_form, 'imgformset' : imgformset, "start": current_date}

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

                            request.session['addPropPopUp'] =  True
                            return redirect('profile') #sair

                        else:
                            listing_form = ListingForm()
                            save_property(request)
                            request.session['listing'] =  True
                            #del request.session['livingrooms_num']

                            imgformset = ImgFormSet(queryset=Image.objects.none())
                            context = {'listing_form': listing_form, 'imgformset' : imgformset, "start": current_date}

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
                            
                            separate= f.cleaned_data.get('separate')
                            print(separate)

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
                                        img_r = img_pli.resize((600,337))
                                        img_r.save(str(img.image))

                            del request.session['prop_serial']

                            try:
                                del request.session['livingrooms_num']
                            except:
                                pass

                            if request.session['l_type'] == 'Apartment' or request.session['l_type'] == 'House':
                                #if f.cleaned_data.get('multiple_listing') == 'whole':
                                apart_obj = Property_listing(main_listing = main_listing, associated_property = assoc_prop)
                                apart_obj.save()
                                
                                

                            elif request.session['l_type'] == 'Bedroom' or request.session['l_type'] == 'Studio':
                                room_obj = Room_listing(
                                    main_listing = main_listing,
                                    associated_room = Bedroom.objects.get(associated_property = assoc_prop))
                                room_obj.save()
                                

                            request.session['addPropPopUp'] =  True
                            return redirect('profile') #sair 


            return redirect('index')     #PLACEHOLDER
                            
        else:
            vars = ['bedrooms_num', 'bathrooms_num', 'kitchens_num', 'livingrooms_num', 'no_living', 'multiple_bedrooms', 'multiple_listing', 'l_type']
            for v in vars:
                try:
                    del request.session[v]
                except:
                    pass

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
    #print('pls_get_in')
    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('profile')

    ag_request = Agreement_Request.objects.get(id=request_id)
    ag_request.accepted = True
    ag_request.save()


    listOfAgreements_ = []
    for e in Agreement_Request.objects.all():
        if e.landlord_id == lord.id:
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
        dateOfRequest_ = a.dateOfRequest
        fullList_.append([id_req, nomeTen, message_, startsDate_, endDate_, accepted_,dateOfRequest_])
    sizeList = len(fullList_)
    reverseList = list(reversed(fullList_))
    #ola = Agreement_Request.objects.get(landlord_id=1)
    #print(ola.tenant_id)
    context = {"fullList_": reverseList, 'range': range(sizeList)}

    return render(request, "mainApp/notificationsLandlord.html", context)

@login_required(login_url='login_view')
def deny_request(request, request_id):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    #print('pls_DONT_get_in')
    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('search')

    ag_request = Agreement_Request.objects.get(id=request_id)
    ag_request.accepted = False
    ag_request.save()

    listOfAgreements_ = []
    for e in Agreement_Request.objects.all():
        if e.landlord_id == lord.id:
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
        dateOfRequest_ = a.dateOfRequest
        fullList_.append([id_req, nomeTen, message_, startsDate_, endDate_, accepted_,dateOfRequest_])
    sizeList = len(fullList_)
    reverseList = list(reversed(fullList_))
    #ola = Agreement_Request.objects.get(landlord_id=1)
    #print(ola.tenant_id)
    context = {"fullList_": reverseList, 'range': range(sizeList)}

    return render(request, "mainApp/notificationsLandlord.html", context)


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
            print(message)
            dateNow = timezone.now()

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
                    message=message,
                    dateOfRequest = dateNow
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
                    message=message,
                    dateOfRequest = dateNow
                )
                ag_request.save()

                return redirect('index')
    else:

        room_id = request.session.get('room_listing')
        prop_id = request.session.get('property_listing')

        if room_id:

            assoc_listing = Room_listing.objects.get(id=room_id)
            main_listing = assoc_listing.main_listing
            start = main_listing.availability_starts.strftime('%Y-%m-%d')
            end = main_listing.availability_ending.strftime('%Y-%m-%d')

            context = {"start": start, "end": end}
        
        else:

            assoc_listing = Property_listing.objects.get(id=prop_id)
            main_listing = assoc_listing.main_listing
            start = main_listing.availability_starts.strftime('%Y-%m-%d')
            end = main_listing.availability_ending.strftime('%Y-%m-%d')

            context = {"start": start, "end": end}

        return render(request, 'mainApp/intent.html', context)

@login_required(login_url='login_view')
def profile(request):
    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    if request.method == 'POST':
        
        user_form = UpdateUserForm(data=request.POST)
        print(user_form.errors)
        if user_form.is_valid():
            current_user.first_name = user_form.cleaned_data.get('first_name')
            current_user.last_name = user_form.cleaned_data.get('last_name')
            current_user.email = user_form.cleaned_data.get('email')
            current_user.save()

            a_user.phoneNumber = user_form.cleaned_data.get('phoneNumber')
            a_user.birthDate = user_form.cleaned_data.get('birthDate')
            a_user.save()

            if request.session['typeUser'] == "Tenant":

                ten_user = Tenant.objects.get(ten_user=a_user)

                ten_user.university = user_form.cleaned_data.get('university')
                ten_user.min_search = user_form.cleaned_data.get('min_search')
                ten_user.max_search = user_form.cleaned_data.get('max_search')
                ten_user.save()
        
        return redirect('index')

    else:
    
        temp = False
        if request.session['typeUser'] == "Tenant":
            for i in Agreement.objects.all():
                if Tenant.objects.get(id = (i.tenant_id)).ten_user_id == a_user.id:
                    #check dates
                    agreement = i
                    endDate = agreement.endDate
                    presentTime = datetime.today().strftime('%d-%m-%Y')
                    now_date = date(int(presentTime.split("-")[2]), int(presentTime.split("-")[1]), int(presentTime.split("-")[0]))
                    diffDates = (endDate - now_date).days
                    temp = True

                    user_birth = a_user.birthDate.strftime('%Y-%m-%d')
                    user_phone = a_user.phoneNumber
                    user_type = _('Inquilino')

                    ten_user = Tenant.objects.get(ten_user=a_user)
                    user_min_search = ten_user.min_search
                    user_max_search = ten_user.max_search
                    user_university = ten_user.university

                    context = {"diffDates": diffDates,
                    "birth": user_birth,
                    "phone": user_phone,
                    "type": user_type,
                    "min": user_min_search,
                    "max": user_max_search,
                    "university": user_university}

            if temp == False:
                context = {}
        else:

            user_birth = a_user.birthDate.strftime('%Y-%m-%d')
            user_phone = a_user.phoneNumber
            user_type = _('Senhorio')

            context = {"birth": user_birth, "phone": user_phone, "type": user_type}

        user_form = UpdateUserForm()
        context['user_form'] = user_form
        return render(request, "mainApp/profile.html", context)

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
    livingrooms_num = Livingroom.objects.filter(associated_property=property_object).count()
    request.session["edit_livingrooms_num"] = livingrooms_num

    if request.method == 'POST':
        f = UpdatePropertyForm(request.POST, instance=property_object)
        print(f.errors)
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
            try:
                property_listing = Property_listing.objects.get(associated_property=property_object)
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
    context = {'bed_formset':bed_formset, 'property_id':property_id, 'bedrooms_info_zip':bedrooms_info_zip, 'bedrooms_num':len(bedrooms_list)}
    return render(request, "mainApp/editBedrooms.html", context)

""" def bedroom_delete_view(request, property_id, bedroom_id=None ):
    try:
        bedroom_object = Bedroom.objects.get(id=bedroom_id)
    except:
        return redirect("/mainApp/profile/propertiesManagement/bedroomsEditing/{}".format(property_id))
    try:
        room_listing = Room_listing.objects.get(associated_room=bedroom_object)
    except:
        room_listing = None

    if room_listing == None:
        bedroom_object.delete()
    
    return redirect("/mainApp/profile/propertiesManagement/bedroomsEditing/{}".format(property_id)) """

def bathrooms_editing_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    bathrooms_queryset = Bathroom.objects.filter(associated_property=property_object)

    if request.method == 'POST':
        bath_formset = BathroomFormSet(request.POST, queryset=bathrooms_queryset)
        if bath_formset.is_valid():
            for form in bath_formset.forms:
                bathroom = form.save(commit="False")
                bathroom.associated_property = property_object
                bathroom.save()

            return redirect("/mainApp/profile/propertiesManagement/kitchensEditing/{}".format(property_object.id))    
    else:        
        bath_formset = BathroomFormSet(queryset=bathrooms_queryset)
        bath_formset.extra=0
    
    context = {'bath_formset':bath_formset, 'property_id':property_id, 'bathrooms_num': len(list(bathrooms_queryset))}
    return render(request, "mainApp/editBathrooms.html", context)

""" def bathroom_delete_view(request, property_id, bathroom_id=None):
    try:
        bathroom_object = Bathroom.objects.get(id=bathroom_id)
    except:
        return redirect("/mainApp/profile/propertiesManagement/bathroomsEditing/{}".format(property_id))
    bathroom_object.delete()
    
    return redirect("/mainApp/profile/propertiesManagement/bathroomsEditing/{}".format(property_id)) """

def kitchens_editing_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    kitchens_queryset = Kitchen.objects.filter(associated_property=property_object)
    livingrooms_num = len(list(Livingroom.objects.filter(associated_property=property_object)))
    print(property_object)
    if request.method == 'POST':
        kitchen_formset = KitchenFormSet(request.POST, queryset=kitchens_queryset)
        if kitchen_formset.is_valid():
            for form in kitchen_formset.forms:
                kitchen = form.save(commit="False")
                kitchen.associated_property = property_object
                kitchen.save()

            if livingrooms_num > 0:
                return redirect("/mainApp/profile/propertiesManagement/livingroomsEditing/{}".format(property_object.id))   
            else:
                return redirect("/mainApp/profile/propertiesManagement")
            del request.session["edit_livingrooms_num"]
            
    else:        
        kitchen_formset = KitchenFormSet(queryset=kitchens_queryset)
        kitchen_formset.extra=0
    
    context = {'kitchen_formset':kitchen_formset, 'property_id':property_id, 'kitchens_num': len(list(kitchens_queryset)), 'livingrooms_num':livingrooms_num}
    return render(request, "mainApp/editKitchens.html", context)

""" def kitchen_delete_view(request, property_id, kitchen_id=None):
    try:
        kitchen_object = Kitchen.objects.get(id=kitchen_id)
    except:
        return redirect("/mainApp/profile/propertiesManagement/kitchensEditing/{}".format(property_id))
    kitchen_object.delete()
    
    return redirect("/mainApp/profile/propertiesManagement/kitchensEditing/{}".format(property_id)) """

def livingrooms_editing_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    livingrooms_queryset = Livingroom.objects.filter(associated_property=property_object)
    if request.method == 'POST':
        livingroom_formset = LivingroomFormSet(request.POST, queryset=livingrooms_queryset)
        if livingroom_formset.is_valid():
            for form in livingroom_formset.forms:
                form.save()    
            return redirect("/mainApp/profile/propertiesManagement")
    else:        
        livingroom_formset = LivingroomFormSet(queryset=livingrooms_queryset)
        livingroom_formset.extra=0

    context = {'live_formset':livingroom_formset, 'property_id':property_id}
    return render(request, "mainApp/editLivingrooms.html", context)


""" def livingroom_delete_view(request, property_id, livingroom_id=None):
    try:
        livingroom_object = Livingroom.objects.get(id=livingroom_id)
    except:
        return redirect("/mainApp/profile/propertiesManagement/livingroomsEditing/{}".format(property_id))
    livingroom_object.delete()
    
    return redirect("/mainApp/profile/propertiesManagement/livingroomsEditing/{}".format(property_id)) """

def listings_management_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    bedrooms = list(Bedroom.objects.filter(associated_property=property_object))
    
    property_listing = None
    main_listing  = []
    #rooms_listing = []

    if request.method == 'POST':
        listing_id = request.POST.get('name')
        #print(request.POST.get("isActive"))
        is_active = 1
        if request.POST.get("isActive") == None:
            is_active = 0
        listing = Listing.objects.get(id=listing_id)
        listing.is_active = is_active
        listing.save()
    #property_listing
    try:
        property_listing = Property_listing.objects.get(associated_property=property_object)
        main_listing.append(property_listing.main_listing)
    except:
        #bedrooms_listing
        try:
            for bedroom in bedrooms:
                room_listing = Room_listing.objects.get(associated_room=bedroom)
                #rooms_listing.append(room_listing)
                main_listing.append(room_listing.main_listing)
        except:
            pass
    context = {'property_listing':property_listing, 'main_listing':main_listing, 'property':property_object}
    return render(request, "mainApp/listingsManagement.html", context)

def listing_editing_view(request, property_id, main_listing_id):
    
    main_listing = Listing.objects.get(id=main_listing_id)
    main_listing.availability_starts = main_listing.availability_starts.strftime('%Y-%m-%d')
    main_listing.availability_ending = main_listing.availability_ending.strftime('%Y-%m-%d')

    image_album = main_listing.album
    
    images = Image.objects.filter(album=image_album)

    if request.method == 'POST':
        f = ListingForm(request.POST, instance=main_listing)
        #f.cleaned_data()
        if f.is_valid():
            f.save()

        imgformset = ImgFormSet(request.POST, request.FILES)
        imgs = imgformset.cleaned_data

        prop_album = main_listing.album

        for d in imgs:
            cover = False
            if len(images) == 0:
                if d == imgs[0]:
                    cover = True

            for i in d.values():
                if i != None:
        
                    img = Image(
                        name= main_listing.title+'_'+str(property_id),
                        is_cover = cover,
                        image = i,
                        album = prop_album)
                    img.save()
                    img_pli = PIL.Image.open(img.image)  
                    img_r = img_pli.resize((600,337))
                    img_r.save(str(img.image)) 

        return redirect("/mainApp/profile/propertiesManagement/listingEditing/{}".format(property_id))

    img_formset = ImgFormSet(queryset=Image.objects.none())
    img_formset.extra=1

    imagesPaths = []
    imagesId = []
    for i in list(images):
        pathSplited = str(i.image).split('mainApp/static/')
        imagesPaths.append(pathSplited[1])
        imagesId.append(i.id)

    imagesZip = zip(imagesPaths, imagesId)
    imagesNum = len(imagesPaths)
    context = {'main_listing':main_listing, 'img_formset':img_formset, "imagesZip":imagesZip, 'editListing':True, "imagesNum": imagesNum}
    return render(request, "mainApp/editListing.html", context)

def remove_image_view(request, property_id, main_listing_id, image_id):
    try:
        image_obj = Image.objects.get(id=image_id)
        image_path = image_obj.image.url
        if os.path.exists(image_path[1:]):
            os.remove(image_path[1:])
        image_obj.delete()

    except :
        pass

    return redirect("/mainApp/profile/propertiesManagement/listingEditing/{}/{}#imagesDiv".format(property_id,main_listing_id))

def create_listing_view(request, property_id):
    property_object = Property.objects.get(id=property_id)

    if request.method == 'POST':
        prop_album = ImageAlbum(name=request.POST.get('title'))
        prop_album.save()
        listing_obj = Listing(
            listing_type = property_object.listing_type,
            allowed_gender = request.POST.get('allowed_gender'),
            monthly_payment =  request.POST.get('monthly_payment'),
            availability_starts =  request.POST.get('availability_starts'),
            availability_ending =  request.POST.get('availability_ending'),
            title =  request.POST.get('title'),
            description =  request.POST.get('description'),
            security_deposit =  request.POST.get('security_deposit'),
            max_capacity =  request.POST.get('max_capacity'),
            is_active = True,
            album = prop_album
        )
        listing_obj.save()

        if listing_obj.listing_type == 'Apartment' or listing_obj.listing_type == 'House':
            property_l_obj = Property_listing(
                associated_property = property_object,
                main_listing = listing_obj
            )
            property_l_obj.save()
        else:
            room_l_obj = Room_listing(
                main_listing  = listing_obj,
                associated_room = Bedroom.objects.get(associated_property = property_object)
            )
            room_l_obj.save()
        
        imgformset = ImgFormSet(request.POST, request.FILES)
        imgs = imgformset.cleaned_data
        
        for d in imgs:
            cover = False
            if d == imgs[0]:
                cover = True

            for i in d.values():
                if i != None:
        
                    img = Image(
                        name= listing_obj.title+'_'+str(property_object.id),
                        is_cover = cover,
                        image = i,
                        album = prop_album)
                    img.save()
                    img_pli = PIL.Image.open(img.image)  
                    img_r = img_pli.resize((600,337))
                    img_r.save(str(img.image)) 

        return redirect("/mainApp/profile/propertiesManagement/listingEditing/{}".format(property_object.id))
    
    img_formset = ImgFormSet(queryset=Image.objects.none())
    img_formset.extra = 1
    context = {'img_formset':img_formset, 'editListing':False}
    return render(request, "mainApp/editListing.html", context)

def delete_listing_view(request, property_id, main_listing_id):
    main_listing_obj = Listing.objects.get(id=main_listing_id)
    if main_listing_obj.listing_type == "Apartment" or main_listing_obj.listing_type == "House":
        property_listing_objs = Property_listing.objects.filter(main_listing=main_listing_obj)
        for e in property_listing_objs:
            e.delete()
    else:
        room_listing_objs = Room_listing.objects.filter(main_listing=main_listing_obj)
        for e in room_listing_objs:
            e.delete()
            
    #delete albuns and photos
    album_obj = main_listing_obj.album
    
    images = Image.objects.filter(album=album_obj)
    for i in images:
        i.delete()
        
    album_obj.delete()

    #delete main_listing
    main_listing_obj.delete()

    #delete images and directory
    folder = 'mainApp/static/mainApp/listings/'+ str(main_listing_id)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete')
    
    os.rmdir(folder)

    return redirect("/mainApp/profile/propertiesManagement/listingEditing/{}".format(property_id))

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
        tenantName = tenant_.ten_user.user.username
        message = a.message 
        startsDate = a.startsDate.strftime("%d-%m-%Y")
        endDate = a.endDate.strftime("%d-%m-%Y")
        accepted = a.accepted #para ver se esta null, aceite ou recusada
        dateOfRequest_ = a.dateOfRequest
        fullList.append([_id_req, nomeLand, message, startsDate, endDate, accepted,dateOfRequest_, tenantName])
    sizeList = len(fullList)
    reverseList = list(reversed(fullList))
    context = {"fullList" : reverseList, "sizeList": sizeList}
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
        startsDate_ = a.startsDate.strftime("%d-%m-%Y")
        endDate_ = a.endDate.strftime("%d-%m-%Y")
        accepted_ = a.accepted #vem sempre a null, pronta a ser definida pelo landlord
        dateOfRequest_ = a.dateOfRequest
        fullList_.append([id_req, nomeTen, message_, startsDate_, endDate_, accepted_,dateOfRequest_])
    sizeList = len(fullList_)
    reverseList = list(reversed(fullList_))
    #ola = Agreement_Request.objects.get(landlord_id=1)
    #print(ola.tenant_id)
    #print(reversed(fullList_))
    context = {"fullList_": reverseList, 'range': range(sizeList)}
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
    rangeList = []
    previewPerPage = 12
    pageNumbers = []

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
            
            queryWhere += " AND l.album_id = i.album_id AND i.is_cover = 1 AND l.is_active = 1"

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
            if any( form.cleaned_data.get('type') == x for x in ('Bedroom', 'Studio')):
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
        tempTuple = row[i][:5] + (row[i][5].split('mainApp/static/')[1],) + row[i][6:] + (round(get_distance(lng_1, lat_1, lng_2, lat_2),1),)
        row = row[:i] + (tempTuple,) + row[i+1:]
        rangeList.append(i)
        if (i % previewPerPage == 0):
            pageNumbers.append(int(i/previewPerPage)+1)

    
    context = {
        'searched_values' : searched_values,  #list with 3 elements containing the coordinates of the searched address and radius of the search 
        'num_results' : len(row), 
        'row' : row,
        'searched' : searched,
        'pageNumbers':  pageNumbers,
        'previewPerPage': previewPerPage,
        'zipPreviews': zip(row, rangeList),
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
            messages.info(request, _('Opção reservada a inquilinos.'), extra_tags='tenant_lock')
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
                listing_name = main_listing.title

            else:
                prop_listing = ag_request.associated_property_listing
                assoc_prop = prop_listing.associated_property
                lord = assoc_prop.landlord
                main_listing = prop_listing.main_listing
                listing_name = main_listing.title

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
            "notify_url": " http://daf7bb482200.ngrok.io/paymentStatus/",
            "return_url": " http://daf7bb482200.ngrok.io/mainApp/search",
            "cancel_return": " http://daf7bb482200.ngrok.io/mainApp/search",

            }

            start_date = ag_request.startsDate
            end_date = ag_request.endDate
            request_id = ag_request.id
            lord_name = lord.lord_user.user.username

            payment_form = PayPalPaymentsForm(initial=paypal_dict)
            context = {
                'pp_form':payment_form,
                'start': start_date,
                'end': end_date,
                'id': request_id,
                'lord_name': lord_name,
                'amount': total_amount,
                'listing_name': listing_name,
                }

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

def emailBody(request):
    return render(request, "mainApp/emailBody.html", {})

def changeLanguage(request):
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            user_language = form.cleaned_data.get('language')
            translation.activate(user_language)
        print(user_language)

def deletePopUp(request):
    request.session['popUp'] =  False
    return render(request, "mainApp/login.html", {})

def deletePopUpProp(request):
    request.session['addPropPopUp'] =  False
    return render(request, "mainApp/profile.html", {})

def renewAgreement(request):
    #FALTA POR A OPÇAO DE RENOVAR A APARECER POR EXEMPLO 1 MES ANTES DO FINAL EM VEZ DE ESTAR SEMPRE VISIVEL

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    
    for i in Agreement.objects.all():
        if Tenant.objects.get(id = (i.tenant_id)).ten_user_id == a_user.id:
            agreement = i
    #print("room " + str(agreement.associated_room_listing_id), "property " +  str(agreement.associated_property_listing_id))
    request.session['room_listing'] = agreement.associated_room_listing_id
    request.session['property_listing'] = agreement.associated_property_listing_id
    request.session["landlord"] = agreement.landlord_id
    request.session["tenant"] = agreement.tenant_id

    #Detalhes do agreement atual
    startDate = agreement.startsDate.strftime('%d-%m-%Y')
    endDate = agreement.endDate.strftime('%d-%m-%Y')
    startDate_v2 = agreement.endDate
    modified_date = startDate_v2 + timedelta(days=1)
    startDate_v3 = modified_date.strftime('%Y-%m-%d')
    prop_test = agreement.associated_property_listing_id
    room_test = agreement.associated_room_listing_id
    landlordName_firststep = Landlord.objects.get(id = agreement.landlord_id).lord_user_id
    landlordName = User.objects.get(id = landlordName_firststep).username 
    
    if prop_test != None:
        propAddress_firststep = Property_listing.objects.get(id = prop_test) 
        propAddress_secndstep = Property.objects.get(id = propAddress_firststep.associated_property_id)
        propAddress = propAddress_secndstep.address
        #print(propAddress)
        context = {"startDate":startDate,"endDate":endDate,"propAddress":propAddress,"landlordName":landlordName,"startDate_v2":startDate_v3}
    else:
        roomAddress_firststep = Room_listing.objects.get(id =room_test)
        roomAddress_secndstep = Bedroom.objects.get(id = roomAddress_firststep.associated_room_id)
        roomAddress_thirdstep = Property.objects.get(id = roomAddress_secndstep.associated_property_id)
        roomAddress = roomAddress_thirdstep.address
        #roomAddress = "1 quarto em " + roomAddress 
        context = {"startDate":startDate,"endDate":endDate,"propAddress":roomAddress,"landlordName":landlordName,"startDate_v2":startDate_v3}
    return render(request, "mainApp/renewAgreement.html", context)

def landlord(request):
    return render(request, "mainApp/landLord.html", {})

def delete_account(request):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    user_type = ''

    try:
        tenant = Tenant.objects.get(ten_user=a_user)
        user_type = 'tenant'
    except:
        lord = Landlord.objects.get(lord_user=a_user)
        user_type = 'lord'

    if user_type == 'tenant':

        for ag in Agreement.objects.all():
            if Tenant.objects.get(id = (ag.tenant_id)).ten_user_id == tenant.ten_user_id:
                
                #falta verificar se o agreement esta ativo
                messages.info(request, _('Ainda possui contratos ativos. Terá de terminar os contratos antes de eliminar os seus dados.'))
                return redirect('index')


        logout(request)
        tenant.delete()
        a_user.delete()
        current_user.delete()
        return redirect('login_view')

    else:

        #to be continued amanha
        pass

    return redirect('index')

def manage_agreements_view(request):
    current_user = request.user
    app_user = App_user.objects.get(user_id = current_user)
    a_user = Landlord.objects.get(lord_user_id=app_user)
    agreement = list(Agreement.objects.filter(landlord = a_user))
    if (agreement[0].associated_room_listing == None):
        listing = agreement[0].associated_property_listing.main_listing.title
    else:
        listing = agreement[0].associated_room_listing.main_listing.title
    print(listing)
    context = {
        "agreement":agreement,
        "listing": listing,
    }
    return render(request, "mainApp/manageAgreements.html", context)

def get_invoice_pdf(request):
    if request.method == 'POST':
        htmlInfo=request.POST['customer_name']
    data = {
        'today': date.today(), 
        'amount': 39.99,
        'customer_name': htmlInfo,
        'order_id': 1233434,
        'phone_number': 967254021,
        'adress': 'Adress',
    }
    pdf = render_to_pdf('mainApp/invoice.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
    