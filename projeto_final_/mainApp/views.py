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
from dateutil.relativedelta import relativedelta
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
                    properties_created = Property.objects.filter(landlord=i)
                    if len(properties_created) == 0:
                        return redirect('landlord')
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
            app_user_object.address = pform.cleaned_data['address']
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
            request.session['redirectPage'] = "login_view"
            return redirect('login_view')  

    context = {'form':form, 'pform': pform, 'errors':form.errors} #, 'pform':pform
    return render(request, 'mainApp/register.html', context)

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
        listing_type = request.session["l_type"],
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
                        bath_serial_list = []
                        if f.is_valid():
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
                        kit_serial_list = []
                        if f.is_valid():
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

                                request.session['popUp'] =  True
                                request.session['redirectPage'] = "profile"
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
                        liv_serial_list = []
                        if f.is_valid():
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

                                request.session['popUp'] =  True
                                request.session['redirectPage'] = "profile"
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
                        bed_serial_list = []
                        if f.is_valid():
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
                        if f.is_valid():
                            separate= f.cleaned_data.get('separate')

                            assoc_prop = Property.objects.get(id=request.session['prop_id'])
                            
                            """ if 'multiple_listing' in f.cleaned_data:
                                if f.cleaned_data.get('multiple_listing') == 'separate':

                                    del request.session['listing']
                                    del request.session['prop_serial']
                                    return redirect('propertiesManagement') """
                            try:
                                prop_album = ImageAlbum(name=f.cleaned_data.get('title')+"_"+str(Listing.objects.all().order_by("-id")[0].id+1))
                            except:
                                prop_album = ImageAlbum(name=f.cleaned_data.get('title')+"_0")
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
                                max_occupancy =  f.cleaned_data.get('max_occupancy'),
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
                                

                            request.session['popUp'] =  True
                            request.session['redirectPage'] = "profile"
                            user_birth = a_user.birthDate.strftime('%Y-%m-%d')
                            user_phone = a_user.phoneNumber
                            context = {"birth": user_birth, "phone": user_phone}
                            
                            return render(request, 'mainApp/profile.html', context=context) #sair 


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
def accept_deny_request(request, request_id):
    ret = redirect('profile')
    if request.method == 'POST':
        formRich = RichTextForm(request.POST)
        if formRich.is_valid():
            if 'accept' in request.POST:
                ret = accept_request(request, request_id, formRich)
            elif 'deny' in request.POST:
                ret = deny_request(request, request_id, formRich)
    return ret

def accept_request(request, request_id, formRich):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('profile')

    ag_request = Agreement_Request.objects.get(id=request_id)
    ag_request.accepted = True
    richText = formRich.save(commit=False)
    richText.save()
    ag_request.messageLandlord = richText
    ag_request.save()

    #INVOICE CREATION
    invoice = Invoice(
        agreement_request = ag_request,
        timestamp = timezone.now(),
        month = timezone.now(),
        paid = False,
        checkReadTenant = False
        )
    invoice.save()

    if ag_request.associated_property_listing == None:
        room_listing = ag_request.associated_room_listing
        main_listing = room_listing.main_listing
    else:
        prop_listing = ag_request.associated_property_listing
        main_listing = prop_listing.main_listing
    
    deposit = main_listing.security_deposit

    invoice_line_deposit = Invoice_Line(
        description = _("Depósito de Entrada"),
        amount = deposit,
        invoice_id = invoice.id,
    )
    invoice_line_deposit.save()

    duration_days = (ag_request.endDate - ag_request.startsDate).days
    if duration_days >= 31:
        total_amount = main_listing.monthly_payment
    else:
        total_amount = int((duration_days/30) * main_listing.monthly_payment)

    invoice_line_rent = Invoice_Line(
        description = _("Renda do mês de ") + _(ag_request.startsDate.strftime("%B")),
        amount = total_amount,
        invoice_id = invoice.id,
    )
    invoice_line_rent.save()

    listOfAgreements_ = []
    for e in Agreement_Request.objects.all():
        if e.landlord_id == lord.id:
            listOfAgreements_.append(e)
            
    for i in listOfAgreements_:
        tempList_prop = Agreement_Request.objects.filter(associated_property_listing = i.associated_property_listing, accepted = None)
        tempList_room = Agreement_Request.objects.filter(associated_room_listing = i.associated_room_listing, accepted = None)
        if (len(tempList_prop) > 1 and i.accepted == True):
            for j in tempList_prop:
                j.accepted = False  # change field
                j.save() # save update
                
        elif (len(tempList_room) > 1 and i.accepted == True):
            for j in tempList_room:
                j.accepted = False #change field
                j.save() #save update

    return redirect('notificationsLandlord')

def deny_request(request, request_id, formRich):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('search')

    ag_request = Agreement_Request.objects.get(id=request_id)
    ag_request.accepted = False
    richText = formRich.save(commit=False)
    richText.save()
    ag_request.messageLandlord = richText
    ag_request.save()

    listOfAgreements_ = []
    for e in Agreement_Request.objects.all():
        if e.landlord_id == lord.id:
            listOfAgreements_.append(e)
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
        checkReadLandlord = a.checkReadLandlord
        try:
            rich = Rich_Text_Message.objects.get(id=a.messageLandlord.id)
            messageLand = rich.message
        except:
            messageLand = _('O senhorio não disponibilizou nenhuma mensagem')
        if a.associated_property_listing != None:
            propertyAddress = a.associated_property_listing.associated_property.address
        else:
            propertyAddress = a.associated_room_listing.associated_room.associated_property.address
        fullList_.append([id_req, nomeTen, message_, startsDate_, endDate_, accepted_,dateOfRequest_, propertyAddress, checkReadLandlord, messageLand,userTen.id])
    sizeList = len(fullList_)
    reverseList = list(reversed(fullList_))

    listOfRefunds = []
    for r in Refund.objects.all():
        if r.landlord == lord:
            listOfRefunds.append(r)
    
    fullListRef = []
    for rb in listOfRefunds:
        id_ref = rb.id
        nameOfTen = (((rb.tenant).ten_user).user).username
        id_ten_ref = (((rb.tenant).ten_user).user).id
        value = rb.value
        startDate = (rb.agreement).startsDate
        plannedFinishDate = (rb.agreement).endDate
        actualFinishDate = rb.dateOfRequest
        check = rb.checkReadLandlord
        status = rb.status
        if (rb.agreement).associated_property_listing != None:
            propertyAddressR = (rb.agreement).associated_property_listing.associated_property.address
        else:
            propertyAddressR = (rb.agreement).associated_room_listing.associated_room.associated_property.address
        fullListRef.append([id_ref,nameOfTen,value,actualFinishDate,propertyAddressR,startDate,plannedFinishDate,check,status,id_ten_ref])
    reverseListRef = list(reversed(fullListRef))
    sizeListRef = len(fullListRef)

    context = {"fullList_": reverseList, 'range': range(sizeList), "fullListRef": reverseListRef,"sizeListRef": sizeListRef}

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
    last_invoice = Invoice.objects.get(agreement_request = ag_request) 
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
            endDate= ag_request.endDate,
            last_invoice_date = last_invoice.timestamp,
            status = True,
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
            endDate= ag_request.endDate,
            last_invoice_date = last_invoice.timestamp,
            status = True,
        )
        new_ag.save()
        assoc_listing.main_listing.is_active = False
        assoc_listing.save()

    last_invoice.agreement = new_ag
    last_invoice.save()

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
            dateNow = timezone.now()
            checkReadLandlord = False
            checkReadTenant = False

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
                    dateOfRequest = dateNow,
                    checkReadLandlord = checkReadLandlord ,
                    checkReadTenant = checkReadTenant
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
                    dateOfRequest = dateNow,
                    checkReadLandlord = checkReadLandlord ,
                    checkReadTenant = checkReadTenant
                )
                ag_request.save()

                return redirect('index')
    else:


        room_id = request.session.get('room_listing')
        prop_id = request.session.get('property_listing')

        if room_id:

            checkRequests = len(Agreement_Request.objects.filter(tenant=ten,associated_room_listing_id=room_id))
            if checkRequests > 0 :
                request.session['onlyOneRequest'] = True
                listing_url = (Room_listing.objects.get(id=room_id)).main_listing_id
                return redirect('listing',listing_url)

            assoc_listing = Room_listing.objects.get(id=room_id)
            main_listing = assoc_listing.main_listing
            start = main_listing.availability_starts.strftime('%Y-%m-%d')
            end = main_listing.availability_ending.strftime('%Y-%m-%d')

            form = RichTextForm()

            context = {"start": start, "end": end, "form": form}
        
        else:

            checkRequests = len(Agreement_Request.objects.filter(tenant=ten,associated_property_listing_id=prop_id))
            if checkRequests > 0 :
                request.session['onlyOneRequest'] = True
                listing_url = (Property_listing.objects.get(id=prop_id)).main_listing_id
                return redirect('listing',listing_url)

            assoc_listing = Property_listing.objects.get(id=prop_id)
            main_listing = assoc_listing.main_listing
            start = main_listing.availability_starts.strftime('%Y-%m-%d')
            end = main_listing.availability_ending.strftime('%Y-%m-%d')

            form = RichTextForm()

            context = {"start": start, "end": end, "form": form}
        
        
        return render(request, 'mainApp/intent.html', context)

@login_required(login_url='login_view')
def profile(request):
    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    if request.method == 'POST':
        
        user_form = UpdateUserForm(data=request.POST)
        
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
                try:
                    if (Tenant.objects.get(id = i.tenant_id)).ten_user_id == a_user.id and i.status == True:

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

                        #in case of a cancelled agreement shows the money which the tenant will get back
                        if i.associated_property_listing_id == None:
                            listingRent = Listing.objects.get(id = Room_listing.objects.get(id=i.associated_room_listing_id).main_listing_id).monthly_payment
                            rent_to_be_returned = round((listingRent / 30) * diffDates,2)
                        else:
                            listingRent = Listing.objects.get(id = Property_listing.objects.get(id=i.associated_property_listing_id).main_listing_id).monthly_payment
                            rent_to_be_returned = round((listingRent / 30) * diffDates,2)


                        context = {"diffDates": diffDates,
                        "birth": user_birth,
                        "phone": user_phone,
                        "type": user_type,
                        "min": user_min_search,
                        "max": user_max_search,
                        "university": user_university,
                        "rent_to_be_returned": rent_to_be_returned}
                    elif (Tenant.objects.get(id = i.tenant_id)).ten_user_id == a_user.id and i.status != True:
                        temp = True

                        user_birth = a_user.birthDate.strftime('%Y-%m-%d')
                        user_phone = a_user.phoneNumber
                        user_type = _('Inquilino')

                        ten_user = Tenant.objects.get(ten_user=a_user)
                        user_min_search = ten_user.min_search
                        user_max_search = ten_user.max_search
                        user_university = ten_user.university


                        context = {"birth": user_birth,
                        "phone": user_phone,
                        "type": user_type,
                        "min": user_min_search,
                        "max": user_max_search,
                        "university": user_university}
                except:
                    pass

            if temp == False:
                user_birth = a_user.birthDate.strftime('%Y-%m-%d')
                user_phone = a_user.phoneNumber
                user_type = _('Inquilino')

                ten_user = Tenant.objects.get(ten_user=a_user)
                user_min_search = ten_user.min_search
                user_max_search = ten_user.max_search
                user_university = ten_user.university


                context = {"birth": user_birth,
                "phone": user_phone,
                "type": user_type,
                "min": user_min_search,
                "max": user_max_search,
                "university": user_university}
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

def kitchens_editing_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    kitchens_queryset = Kitchen.objects.filter(associated_property=property_object)
    livingrooms_num = len(list(Livingroom.objects.filter(associated_property=property_object)))

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

def listings_management_view(request, property_id):
    property_object = Property.objects.get(id=property_id)
    bedrooms = list(Bedroom.objects.filter(associated_property=property_object))
    
    property_listing = None
    main_listing  = []

    if request.method == 'POST':
        listing_id = request.POST.get('name')
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

    cannot_removed = False
    try:
        if request.session["cannot_remove_agreement"]:
            cannot_removed = True
            request.session["cannot_remove_agreement"] = False
    except:
        request.session["cannot_remove_agreement"] = False
        
    context = {'property_listing':property_listing, 'main_listing':main_listing, 'property':property_object, "cannot_removed":cannot_removed}
    return render(request, "mainApp/listingsManagement.html", context)

def listing_editing_view(request, property_id, main_listing_id):
    main_listing = Listing.objects.get(id=main_listing_id)
    main_listing.availability_starts = main_listing.availability_starts.strftime('%Y-%m-%d')
    main_listing.availability_ending = main_listing.availability_ending.strftime('%Y-%m-%d')

    image_album = main_listing.album
    
    images = Image.objects.filter(album=image_album)

    if request.method == 'POST':
        f = ListingForm(request.POST, instance=main_listing)
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

    current_date = datetime.today().strftime('%Y-%m-%d')

    context = {'main_listing':main_listing, 'img_formset':img_formset, "imagesZip":imagesZip, 'editListing':True, "imagesNum": imagesNum, "current_date":current_date}
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
            max_occupancy =  request.POST.get('max_occupancy'),
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
        
        #add images to database
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

    current_date = datetime.today().strftime('%Y-%m-%d')

    context = {'img_formset':img_formset, 'editListing':False, "current_date":current_date}
    return render(request, "mainApp/editListing.html", context)

def delete_listing_view(request, property_id, main_listing_id):
    main_listing_obj = Listing.objects.get(id=main_listing_id)

    can_deleted = True
    is_property_listing = True
    is_room_listing = False

    if main_listing_obj.listing_type == "Apartment" or main_listing_obj.listing_type == "House":
        #property_listing
        is_room_listing = False
        property_listing_obj = Property_listing.objects.filter(main_listing=main_listing_obj)[0]
        agreements = Agreement.objects.filter(associated_property_listing=property_listing_obj)
        for agreement in agreements:
            if agreement.status:
                can_deleted = False
                break
    else:
        #room_listing
        is_property_listing = False
        room_listing_obj = Room_listing.objects.filter(main_listing=main_listing_obj)[0]
        agreements = Agreement.objects.filter(associated_room_listing=room_listing_obj)
        for agreement in agreements:
            if agreement.status:
                can_deleted = False
                break

    if can_deleted:
        if is_property_listing:
            property_listing_obj.delete()
        else:
            room_listing_obj.delete()
                
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
                pass
        
        os.rmdir(folder)
    else:
        #cannot be removed
        request.session['cannot_remove_agreement'] = True

    return redirect("/mainApp/profile/propertiesManagement/listingEditing/{}".format(property_id))

def notificationsTenant(request):
    current_user_ = request.user
    a_user_ = App_user.objects.get(user_id=current_user_)
    invoice_id = None

    try:
        tenant_ = Tenant.objects.get(ten_user=a_user_)
    except:
        return redirect('profile')

    listOfAgreements = []
    for e in Agreement_Request.objects.all():
        if e.tenant_id == tenant_.id:
            listOfAgreements.append(e)

    fullList = []
    for a in listOfAgreements:
        _id_req = a.id
        _landlord_ = a.landlord #objeto landlord
        _userLand_ = _landlord_.lord_user
        userLand = _userLand_.user
        nomeLand = userLand.username
        message = a.message 
        startsDate = a.startsDate.strftime("%d-%m-%Y")
        endDate = a.endDate.strftime("%d-%m-%Y")
        accepted = a.accepted #para ver se esta null, aceite ou recusada
        dateOfRequest_ = a.dateOfRequest
        checkReadTenant = a.checkReadTenant
        try:
            rich = Rich_Text_Message.objects.get(id=a.messageLandlord.id)
            messageLand = rich.message
        except:
            messageLand = _('O senhorio não disponibilizou nenhuma mensagem')
        if a.associated_property_listing != None:
            propertyAddress = a.associated_property_listing.associated_property.address
        else:
            propertyAddress = a.associated_room_listing.associated_room.associated_property.address
        try:
            invoice_id = Invoice.objects.get(agreement_request_id=a.id).id
        except:
            pass
        fullList.append([_id_req, nomeLand, message, startsDate, endDate, accepted, dateOfRequest_, invoice_id, propertyAddress,checkReadTenant, messageLand,userLand.id])

    invoiceList = []
    for i in Invoice.objects.all():
        if i.agreement_request == None:
            a = Agreement.objects.get(id=i.agreement_id)
            if a.tenant_id == tenant_.id:
                nameLand = a.landlord.lord_user.user.username
                land_id=a.landlord.lord_user.user.id
                invoiceDate = i.timestamp
                paymentLimit = invoiceDate + timedelta(days=10)
                invoiceMonth = _(i.month.strftime("%B"))
                checkReadTenInv = i.checkReadTenant

                if a.associated_property_listing == None:
                    room_listing = a.associated_room_listing
                    assoc_room = room_listing.associated_room
                    assoc_prop = assoc_room.associated_property
                    main_listing = room_listing.main_listing

                else:
                    prop_listing = a.associated_property_listing
                    assoc_prop = prop_listing.associated_property
                    main_listing = prop_listing.main_listing

                address = assoc_prop.address
                listing_name = main_listing.title

                invoiceList.append([nameLand, invoiceMonth, invoiceDate, paymentLimit, address, listing_name, i.id,checkReadTenInv,land_id])
    
    paymentWarningList = []
    for w in Payment_Warning.objects.all():
        a = Agreement.objects.get(id=w.agreement_id)
        if a.tenant_id == tenant_.id:
            nameLand = a.landlord.lord_user.user.username
            idLand_warn = a.landlord.lord_user.user.id
            checkReadTenWarn = w.checkReadTenant
            if a.associated_property_listing == None:
                room_listing = a.associated_room_listing
                assoc_room = room_listing.associated_room
                assoc_prop = assoc_room.associated_property
                main_listing = room_listing.main_listing

            else:
                prop_listing = a.associated_property_listing
                assoc_prop = prop_listing.associated_property
                main_listing = prop_listing.main_listing

            address = assoc_prop.address
            listing_name = main_listing.title
            timestamp = w.timestamp

            paymentWarningList.append([timestamp, nameLand, address, listing_name,checkReadTenWarn,w.id,idLand_warn])

    reverseList = list(reversed(fullList))

    user_incidences = Incidence.objects.filter(agreement__in=Agreement.objects.filter(tenant = tenant_)).filter(is_read = False)
    
    context = {"fullList" : reverseList, "sizeFull": len(fullList), "invoiceList": invoiceList, "sizeInvoice":len(invoiceList), "paymentWarningList": paymentWarningList, "sizeWarning":len(paymentWarningList), "incidences":user_incidences}
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
        accepted_ = a.accepted 
        dateOfRequest_ = a.dateOfRequest
        checkReadLandlord = a.checkReadLandlord
        try:
            rich = Rich_Text_Message.objects.get(id=a.messageLandlord.id)
            messageLand = rich.message
        except:
            messageLand = _('O senhorio não disponibilizou nenhuma mensagem')
        if a.associated_property_listing != None:
            propertyAddress = a.associated_property_listing.associated_property.address
        else:
            propertyAddress = a.associated_room_listing.associated_room.associated_property.address
        fullList_.append([id_req, nomeTen, message_, startsDate_, endDate_, accepted_,dateOfRequest_, propertyAddress,checkReadLandlord, messageLand, userTen.id])
    sizeList = len(fullList_)
    reverseList = list(reversed(fullList_))

    listOfRefunds = []
    for r in Refund.objects.all():
        if r.landlord == landlord_:
            listOfRefunds.append(r)
    
    fullListRef = []
    for rb in listOfRefunds:
        id_ref = rb.id
        nameOfTen = (((rb.tenant).ten_user).user).username
        id_ten_ref = (((rb.tenant).ten_user).user).id
        value = rb.value
        startDate = (rb.agreement).startsDate
        plannedFinishDate = (rb.agreement).endDate
        actualFinishDate = rb.dateOfRequest
        check = rb.checkReadLandlord
        status = rb.status
        if (rb.agreement).associated_property_listing != None:
            propertyAddressR = (rb.agreement).associated_property_listing.associated_property.address
        else:
            propertyAddressR = (rb.agreement).associated_room_listing.associated_room.associated_property.address
        fullListRef.append([id_ref,nameOfTen,value,actualFinishDate,propertyAddressR,startDate,plannedFinishDate,check,status,id_ten_ref])
    reverseListRef = list(reversed(fullListRef))
    sizeListRef = len(fullListRef)

    form = RichTextForm()

    context = {"fullList_": reverseList, 'range': range(sizeList), "fullListRef": reverseListRef, "sizeListRef": sizeListRef, "form": form}
    return render(request, "mainApp/notificationsLandlord.html", context)

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
    geolocator = MapBox(config('MAPBOX_KEY'), scheme=None, user_agent=None, domain='api.mapbox.com')
    location = ''
    row = ''
    searched = False
    rangeList = []
    previewPerPage = 12
    pageNumbers = []

    searched_values = []
    
    if request.user.is_authenticated:
        current_user = request.user
        app_user = App_user.objects.get(user=request.user)
        try:
            tenant = Tenant.objects.get(ten_user_id=app_user.id)
            location = tenant.university + ", Portugal"
            form = SearchForm(initial = {"location":location, "radius":10, "minPrice":tenant.min_search, "maxPrice":tenant.max_search})
        except:
            form = SearchForm()
    else:
        form = SearchForm()

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
                queryWhere += " AND l.max_occupancy = '" + form.cleaned_data.get('num_tenants') + "'"
            elif(form.cleaned_data.get('num_tenants') == '5'):
                queryWhere += " AND l.max_occupancy >= 5"

            #Date in is filled
            if form.cleaned_data.get('date_in') is not None:
                queryWhere += " AND '" + str(form.cleaned_data.get('date_in')) + "' >= l.availability_starts"
            
            #Date out is filled
            if form.cleaned_data.get('date_out') is not None:
                queryWhere += " AND '" + str(form.cleaned_data.get('date_out')) + "' <= l.availability_ending"

            #Number of bedrooms is filled
            if any(form.cleaned_data.get('num_bedrooms') == x for x in ('1','2','3','4')):
                queryWhere += " AND p.bedrooms_num = '" + form.cleaned_data.get('num_bedrooms') + "'"
            elif(form.cleaned_data.get('num_bedrooms') == '5'):
                queryWhere += " AND p.bedrooms_num >= 5"
            
            #Property type is filled and is either Bedroom, Studio or Residency
            if any( form.cleaned_data.get('type') == x for x in ('Bedroom', 'Studio')):
                queryFrom += ', mainApp_room_listing AS rl'
                queryWhere += " AND l.listing_type = '" + form.cleaned_data.get('type') + "'\
                                AND rl.associated_room_id = p.id AND rl.main_listing_id = l.id"
                cursor.execute(querySelect + queryFrom + queryWhere)
                row = cursor.fetchall()

            #Property type is filled and is either Apartment or House
            elif any( form.cleaned_data.get('type') == x for x in ('Apartment', 'House')):
                queryFrom += ', mainApp_property_listing AS pl'
                queryWhere += " AND l.listing_type = '" + form.cleaned_data.get('type') + "'\
                                AND pl.associated_property_id = p.id AND pl.main_listing_id = l.id"
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
        'searchForm':form,
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
        "land_id": landlord_user.id,
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

            if len(Invoice.objects.filter(agreement_request=ag_request)) <= 1:

                total_amount = main_listing.monthly_payment + main_listing.security_deposit

            else:
                total_amount = main_listing.monthly_payment

            paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": total_amount,
            "currency_code": "EUR",
            "no_note": "1",
            "item_name": main_listing.title,
            "item_number": ag_request.id,
            "custom": current_user.id,
            "notify_url": "http://7523997b61b8.ngrok.io/paymentStatus/",
            "return_url": "http://7523997b61b8.ngrok.io/mainApp/search",
            "cancel_return": "http://7523997b61b8.ngrok.io/mainApp/profile",

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

@login_required(login_url='login_view')
#NESTE MOMENTO ESTAMOS A PAGAR AO SITE EM VEZ DE PAGAR O INQUILINO O VALOR DO REFUND
def make_payment_refunds(request, ref_id):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    try:
        landlord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('search')

    if request.method == 'POST':

        ref = Refund.objects.get(id=ref_id)
        if ref.landlord == landlord:

            if (ref.agreement).associated_property_listing == None:
                room_listing = (ref.agreement).associated_room_listing
                assoc_room = room_listing.associated_room
                assoc_prop = assoc_room.associated_property
                lord = assoc_prop.landlord
                main_listing = room_listing.main_listing
                listing_name = main_listing.title

            else:
                prop_listing = (ref.agreement).associated_property_listing
                assoc_prop = prop_listing.associated_property
                lord = assoc_prop.landlord
                main_listing = prop_listing.main_listing
                listing_name = main_listing.title

            ten_receiver_email = (((ref.tenant).ten_user).user).email
            duration_days = (ref.dateOfRequest.date() - ref.agreement.startsDate).days

            # if len(Invoice.objects.filter(agreement_request=ag_request)) <= 1:

            #     total_amount = main_listing.monthly_payment + main_listing.security_deposit

            # else:
            #     total_amount = main_listing.monthly_payment
            total_amount = ref.value

            paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": total_amount,
            "currency_code": "EUR",
            "no_note": "1",
            "item_name": main_listing.title,
            "item_number": ref.id,
            "custom": current_user.id,
            "notify_url": "http://7523997b61b8.ngrok.io/paymentStatusRef/",
            "return_url": "http://7523997b61b8.ngrok.io/mainApp/search",
            "cancel_return": "http://7523997b61b8.ngrok.io/mainApp/profile",

            }

            start_date = (ref.agreement).startsDate
            end_date = ref.dateOfRequest
            ref_id = ref.id
            ten_name = (((ref.tenant).ten_user).user).username

            payment_form = PayPalPaymentsForm(initial=paypal_dict)
            context = {
                'pp_form':payment_form,
                'start': start_date,
                'end': end_date,
                'id': ref_id,
                'ten_name': ten_name,
                'amount': total_amount,
                'listing_name': listing_name,
                }

            return render(request, template_name='mainApp/paymentRefunds.html', context=context)
        
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
            invoice = Invoice.objects.filter(agreement_request=ag_request_id).order_by("-id")[0]
            invoice.paid = True
            invoice.save()
            
            receipt = Receipt(
                invoice_id = invoice.id
            )
            receipt.save()

            try:
                warning = Payment_Warning.objects.get(invoice=invoice)
                warning.delete()
            except:
                pass

    return redirect('index')

valid_ipn_received.connect(get_payment_status)
invalid_ipn_received.connect(get_payment_status)

@csrf_exempt
def get_payment_status_refunds(sender, **kwargs):
    ipn_obj = sender.POST
    if ipn_obj['payment_status'] == ST_PP_COMPLETED:

        if ipn_obj['receiver_email'] == settings.PAYPAL_RECEIVER_EMAIL:

            ref_id = ipn_obj['item_number']
            user_id = ipn_obj['custom']
            Refund.objects.filter(id=ref_id).update(status=True)
            # invoice = Invoice.objects.filter(agreement_request=ag_request_id).order_by("-id")[0]
            # invoice.paid = True
            # invoice.save()

            # try:
            #     warning = Payment_Warning.objects.get(invoice=invoice)
            #     warning.delete()
            # except:
            #     pass

    return redirect('index')

valid_ipn_received.connect(get_payment_status_refunds)
invalid_ipn_received.connect(get_payment_status_refunds)


def emailBody(request):
    return render(request, "mainApp/emailBody.html", {})

def changeLanguage(request):
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            user_language = form.cleaned_data.get('language')
            translation.activate(user_language)

def deletePopUp(request):
    request.session['popUp'] =  False
    return redirect(request.session['redirectPage'])

def renewAgreement(request):
    #FALTA POR A OPÇAO DE RENOVAR A APARECER POR EXEMPLO 1 MES ANTES DO FINAL EM VEZ DE ESTAR SEMPRE VISIVEL

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    
    for i in Agreement.objects.all():
        if Tenant.objects.get(id = (i.tenant_id)).ten_user_id == a_user.id:
            agreement = i
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
        context = {"startDate":startDate,"endDate":endDate,"propAddress":propAddress,"landlordName":landlordName,"startDate_v2":startDate_v3}
    else:
        roomAddress_firststep = Room_listing.objects.get(id =room_test)
        roomAddress_secndstep = Bedroom.objects.get(id = roomAddress_firststep.associated_room_id)
        roomAddress_thirdstep = Property.objects.get(id = roomAddress_secndstep.associated_property_id)
        roomAddress = roomAddress_thirdstep.address
        #roomAddress = "1 quarto em " + roomAddress 
        context = {"startDate":startDate,"endDate":endDate,"propAddress":roomAddress,"landlordName":landlordName,"startDate_v2":startDate_v3}
    return render(request, "mainApp/renewAgreement.html", context)

@login_required(login_url='login_view')
def landlord(request):
    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('index')
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

                if ag.status == True:

                    messages.info(request, _('Ainda possui contratos ativos. Terá de terminar os contratos antes de eliminar os seus dados.'))
                    return redirect('index')


        logout(request)
        tenant.delete()
        a_user.delete()
        current_user.delete()
        return redirect('login_view')

    else:
        
        for ag in Agreement.objects.all():
            if Landlord.objects.get(id = (ag.landlord_id)).lord_user_id == lord.lord_user_id:

                if ag.status == True:

                    messages.info(request, _('Ainda possui contratos ativos. Terá de terminar os contratos antes de eliminar os seus dados.'))
                    return redirect('index')

        
        for p_listing in Property_listing.objects.all():
            assoc_prop = Property.objects.get(id=p_listing.associated_property.id)

            if assoc_prop.landlord.id == lord.id:
                main_listing = p_listing.main_listing
                listing_album = main_listing.album
                listing_album.delete()
                #main_listing will be auto deleted after this

        for r_listing in Room_listing.objects.all():
            assoc_room = Bedroom.objects.get(id=r_listing.associated_room.id)
            assoc_prop = assoc_room.associated_property

            if assoc_prop.landlord.id == lord.id:
                main_listing = r_listing.main_listing
                listing_album = main_listing.album
                listing_album.delete()
                #main_listing will be auto deleted after this

        logout(request)
        lord.delete()
        a_user.delete()
        current_user.delete()
        return redirect('login_view')

    return redirect('index')

def manage_agreements_view(request):
    current_user = request.user
    app_user = App_user.objects.get(user_id = current_user)
    a_user = Landlord.objects.get(lord_user_id=app_user)
    agreement = Agreement.objects.filter(landlord = a_user)

    listing = ""

    listAgreementAndPaid = []
    for a in agreement:
        send_invoice = True
        month = a.last_invoice_date.replace(day=1) + relativedelta(months=1)
        payment_warning = 'paid'
        invoices_warning = []

        if (a.associated_room_listing == None):
            listing = a.associated_property_listing.main_listing.title
        else:
            listing = a.associated_room_listing.main_listing.title
        if (a.last_invoice_date.strftime("%B") == timezone.now().strftime("%B")):
            send_invoice = False
        
        invoices = Invoice.objects.filter(agreement_id = a.id)

        #Adds late payments to the invoices_warning list
        for i in invoices:
                if i.paid == 0:
                    if (timezone.now().date() - i.timestamp).days >= 10:
                        payment_warning = True
                        invoices_warning.append(i.id)
                    elif payment_warning == 'paid':
                        payment_warning = None

        #Removes from invoices_warning list any late payments already warned
        for w in Payment_Warning.objects.all():
            if w.invoice_id in invoices_warning:
                invoices_warning.remove(w.invoice_id)
                payment_warning = False

        #If there are any not warned late payments
        if len(invoices_warning) > 0:
            payment_warning = True
        #If there are late payments but already warned
        elif len(invoices_warning) == 0 and payment_warning == True:
            payment_warning = False      

        listAgreementAndPaid.append([a, send_invoice, _(month.strftime("%B")), payment_warning])

    context = {
        "listAgreementAndPaid":listAgreementAndPaid,
        "listing": listing,
        'type': 'landlord',
    }
    return render(request, "mainApp/manageAgreements.html", context)

def get_invoice_pdf(request):
    if request.method == 'POST':
        invoice_id=request.POST['invoice_id']
        if invoice_id != None:
            total = 0

            invoice = Invoice.objects.get(id=invoice_id)
            if (invoice.agreement_id == None):
                ag = Agreement_Request.objects.get(id=invoice.agreement_request_id)
            else:
                ag = Agreement.objects.get(id=invoice.agreement_id)
            tenant = Tenant.objects.get(id=ag.tenant_id)
            tenant_app = App_user.objects.get(user_id=tenant.ten_user_id)
            tenant_user = User.objects.get(id=tenant_app.user_id)
            list_invoice_line = Invoice_Line.objects.filter(invoice_id = invoice_id)

            for line in list_invoice_line:
                total += line.amount

            data = {
                'today': invoice.timestamp, 
                'customer_name': str(tenant_user.first_name) + " " + str(tenant_user.last_name),
                'order_id': invoice.id,
                'phone_number': tenant_app.phoneNumber,
                'adress': tenant_app.address,
                'list_lines': list_invoice_line,
                'total_amount': total,
            }
            pdf = render_to_pdf('mainApp/invoicePDF.html', data)
            return HttpResponse(pdf, content_type='application/pdf')

def invoicesLandlord(request):
    context={}

    if request.method == 'POST':
        agreement=request.POST['agreement_id']

        list_invoices = Invoice.objects.filter(agreement_id = agreement)

        fullList = []
        for i in list_invoices:
            payment_warning = None
            if i.paid == 0:
                if (timezone.now().date() - i.timestamp).days >= 10:
                    payment_warning = True
            else:
                payment_warning = 'paid'
            
            for w in Payment_Warning.objects.all():
                if w.invoice_id == i.id:
                    payment_warning = False
            
            fullList.append([i, payment_warning])
        context={
            'fullList': fullList,
            'agreement': agreement,
            'type': 'landlord',
        }
 
    return render(request, "mainApp/invoices.html", context)

def send_invoice(request):
    if request.method == 'POST':
        agreement_id=request.POST['agreement_id']

        agreement = Agreement.objects.get(id=agreement_id)

        #INVOICE CREATION
        if (agreement.last_invoice_date.strftime("%B") != timezone.now().strftime("%B")):
            new_date = agreement.last_invoice_date
            new_date = new_date.replace(day=1) + relativedelta(months=1)
            agreement.last_invoice_date = new_date
            agreement.save()

            if agreement.associated_property_listing == None:
                room_listing = agreement.associated_room_listing
                main_listing = room_listing.main_listing
            else:
                prop_listing = agreement.associated_property_listing
                main_listing = prop_listing.main_listing

            if agreement.last_invoice_date.strftime("%B") == agreement.endDate.strftime("%B"):
                duration_days = (agreement.endDate - agreement.last_invoice_date).days
                total_amount = int((duration_days/30) * main_listing.monthly_payment)
            else:
                total_amount = main_listing.monthly_payment

            timestamp = timezone.now()

            invoice = Invoice(
                agreement = agreement,
                timestamp = timestamp,
                month = new_date,
                paid = False,
                checkReadTenant = False
            )
            invoice.save()

            invoice_line_rent = Invoice_Line(
                description = _("Renda do mês de ") + _(new_date.strftime("%B")),
                amount = total_amount,
                invoice_id = invoice.id,
            )
            invoice_line_rent.save()
  
    return redirect('manage_agreements_view')

def send_payment_warning(request):
    if request.method == 'POST':
        agreement_id=request.POST['agreement_id']
        invoice_id=request.POST['invoice_id']

        agreement = Agreement.objects.get(id=agreement_id)
        invoice = Invoice.objects.get(id=invoice_id)

        try:
            pw =  Payment_Warning.objects.get(invoice_id=invoice_id)
        except:
            warning = Payment_Warning(
                agreement_id = agreement.id,
                timestamp = timezone.now(),
                invoice_id = invoice.id,
                checkReadTenant = False
            )
            warning.save()
            request.session['popUp'] =  True
            request.session['redirectPage'] = 'manage_agreements_view'
    return redirect('manage_agreements_view')

def manageAgreementsTenant(request):
    current_user = request.user
    app_user = App_user.objects.get(user_id = current_user)
    a_user = Tenant.objects.get(ten_user_id=app_user)
    agreement = Agreement.objects.filter(tenant = a_user)

    listing = ""

    listAgreementAndPaid = []
    for a in agreement:
        send_invoice = True
        month = a.last_invoice_date.replace(day=1) + relativedelta(months=1)
        payment_warning = None

        if (a.associated_room_listing == None):
            listing = a.associated_property_listing.main_listing.title
        else:
            listing = a.associated_room_listing.main_listing.title
        if (a.last_invoice_date.strftime("%B") == timezone.now().strftime("%B")):
            send_invoice = False
        
        invoices = Invoice.objects.filter(agreement_id = a.id)

        #Checks for none paid
        for i in invoices:
            if i.paid == 0:
                 payment_warning = False

            #Checks if there are any warnings
            for w in Payment_Warning.objects.all():
                if w.invoice_id == i.id:
                    payment_warning = True 

        listAgreementAndPaid.append([a, send_invoice, _(month.strftime("%B")), payment_warning])

    context = {
        "listAgreementAndPaid":listAgreementAndPaid,
        "listing": listing,
        'type': 'tenant',
    }
    return render(request, "mainApp/manageAgreements.html", context)

def invoicesTenant(request):
    context={}

    if request.method == 'POST':
        agreement=request.POST['agreement_id']

        list_invoices = Invoice.objects.filter(agreement_id = agreement)

        fullList = []
        for i in list_invoices:
            payment_warning = None
            for w in Payment_Warning.objects.all():
                if w.invoice_id == i.id:
                    payment_warning = True
            if i.paid == 1:
                payment_warning = False
            
            fullList.append([i, payment_warning])
        context={
            'fullList': fullList,
            'agreement': agreement,
            'type': 'tenant',
        }
 
    return render(request, "mainApp/invoices.html", context)

def tenant(request):
    return render(request, "mainApp/tenant.html", {})

def deleteAgreement(request):
    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    try:
        tenant = Tenant.objects.get(ten_user=a_user)
    except:
        return redirect('index')

    for i in Agreement.objects.all():
        if i.tenant_id == tenant.id:
            #check if there are payments due
            if len(Payment_Warning.objects.filter(agreement=i)) > 0 :
                request.session['duePayments'] = True
                return redirect('profile')

            #check dates
            agreement = i
            endDate = agreement.endDate
            presentTime = datetime.today().strftime('%d-%m-%Y')
            now_date = date(int(presentTime.split("-")[2]), int(presentTime.split("-")[1]), int(presentTime.split("-")[0]))
            diffDates = (endDate - now_date).days

            if i.associated_property_listing_id == None:
                listingRent = Listing.objects.get(id = Room_listing.objects.get(id=i.associated_room_listing_id).main_listing_id).monthly_payment
                rent_to_be_returned = round((listingRent / 30) * diffDates,2)
            else:
                listingRent = Listing.objects.get(id = Property_listing.objects.get(id=i.associated_property_listing_id).main_listing_id).monthly_payment
                rent_to_be_returned = round((listingRent / 30) * diffDates,2)
            
            Agreement.objects.filter(id=i.id).update(status=False)
            dateNow = timezone.now()
            refund_obj = Refund(
            value = rent_to_be_returned,
            tenant = tenant,
            landlord = i.landlord,
            agreement = i,
            status = False, #hasnt been paid yet
            checkReadLandlord = False, #hasnt been read yet
            dateOfRequest = dateNow 
            )
            refund_obj.save()        

    return redirect('profile')

def requestPop(request):
    request.session['onlyOneRequest'] = False
    room_id = request.session.get('room_listing')
    prop_id = request.session.get('property_listing')

    if room_id:
        listing_url = (Room_listing.objects.get(id=room_id)).main_listing_id
    else:
        listing_url = (Property_listing.objects.get(id=prop_id)).main_listing_id

    return redirect('listing',listing_url)

def checkReadLandlord(request,id_req):
    if request.method == 'POST':
        for e in Agreement_Request.objects.all():
            if e.id == id_req:
                e.checkReadLandlord = True
                e.save()

        response_data = {}
        response_data['result'] = 'View successful!'

        return HttpResponse(response_data)

def checkReadTenant(request,id_req):

    for e in Agreement_Request.objects.all():
        if e.id == id_req:
            e.checkReadTenant = True
            e.save()

    return redirect('notificationsTenant')

@login_required(login_url='login_view')
def chat_list_view(request):
    request.session["chat_is_new"] = False
    user = request.user
    user_id = user.id
    username = user.username
    if request.is_ajax and request.method == 'GET':
        form = GetChat(request.GET)
        if form.is_valid():
            chat_id = form.cleaned_data.get("chat_id")
            chat_obj = Chat.objects.get(id=chat_id)

            messages = sorted(list(Message.objects.filter(chat=chat_obj)), key=lambda x: x.timestamp, reverse=True)
            result = {}
            result["messages"] = {}
            result["username"] = username
            result["receiver"] = chat_obj.user_1.first_name +" "+ chat_obj.user_1.last_name if chat_obj.user_2.id == user_id else chat_obj.user_2.first_name +" "+ chat_obj.user_2.last_name
            messages_sorted = []
            for m in messages:
                message_dict = m.as_json()
                messages_sorted.append(m.id)
                result["messages"][m.id] = message_dict
            return HttpResponse(json.dumps(result))

    if request.is_ajax and request.method == 'POST':
        form = SendMessage(request.POST)
        if form.is_valid():
            chat = Chat.objects.get(id=form.cleaned_data.get("chat_id"))
            message = Message(
                    chat = chat, 
                    sender = user, 
                    timestamp = timezone.now(),
                    content = form.cleaned_data.get("content"),
                    is_read = False)
            message.save()
            messages = sorted(list(Message.objects.filter(chat=chat)), key=lambda x: x.timestamp, reverse=True)
            result = {}
            result["messages"] = {}
            result["username"] = username
            result["receiver"] = chat.user_1.first_name +" "+ chat.user_1.last_name if chat.user_2.id == user_id else chat.user_2.first_name +" "+ chat.user_2.last_name
            messages_sorted = []
            for m in messages:
                message_dict = m.as_json()
                messages_sorted.append(m.id)
                result["messages"][m.id] = message_dict 
            return HttpResponse(json.dumps(result))

    if request.method == 'POST':
        form = CreateChat(request.POST)
        chat_id = None

        if form.is_valid():
            receiver_id = form.cleaned_data.get("receiver")
            receiver = User.objects.get(id=receiver_id)
            chats_1 = Chat.objects.filter(user_1=receiver, user_2=request.user)
            chats_2 = Chat.objects.filter(user_1=request.user, user_2=receiver)
            if len(chats_1) == 0 and len(chats_2) == 0:
                chat = Chat(
                    user_1=request.user,
                    user_2=receiver,
                    last_message=timezone.now()
                )
                chat.save()
                request.session['chat_is_new'] = True
                chat_id = "#chat_" + str(chat.id)
            else:
                request.session['chat_is_new'] = True
                if len(chats_1) != 0:
                    chat_id = "#chat_" + str(chats_1[0].id)
                else:
                    chat_id = "#chat_" + str(chats_2[0].id)
            
        chats_1 = list(Chat.objects.filter(user_1=user_id))
        chats_2 = list(Chat.objects.filter(user_2=user_id))

        chats_dict = {}

        for c in chats_1:
            chats_dict[c] = c.user_2.first_name + " " + c.user_2.last_name

        for c in chats_2:
            chats_dict[c] = c.user_1.first_name + " " + c.user_1.last_name

        chats_sorted = sorted(chats_dict.keys(), key=lambda x: x.last_message, reverse=True)
        
        if chat_id == None:
            context = {"chats_sorted":chats_sorted, "chats_dict":chats_dict}
        else:
            context = {"chats_sorted":chats_sorted, "chats_dict":chats_dict, "chat_id":chat_id}

        return render(request, "mainApp/chatsList.html", context)

    chats_1 = list(Chat.objects.filter(user_1=user_id))
    chats_2 = list(Chat.objects.filter(user_2=user_id))

    chats_dict = {}

    for c in chats_1:
        chats_dict[c] = c.user_2.first_name + " " + c.user_2.last_name

    for c in chats_2:
        chats_dict[c] = c.user_1.first_name + " " + c.user_1.last_name

    chats_sorted = sorted(chats_dict.keys(), key=lambda x: x.last_message, reverse=True)
    context = {"chats_sorted":chats_sorted, "chats_dict":chats_dict}

    return render(request, "mainApp/chatsList.html", context)

def checkReadLandlordRef(request,id_ref):
    if request.method == 'POST':
        for r in Refund.objects.all():
            if r.id == id_ref:
                r.checkReadLandlord = True
                r.save()
        response_data = {}
        response_data['result'] = 'View successful!'

        return HttpResponse(response_data)

def checkReadTenantInvoice(request,id_inv):
    if request.method == 'POST':
        for i in Invoice.objects.all():
            if i.id == id_inv:
                i.checkReadTenant = True
                i.save()
        response_data = {}
        response_data['result'] = 'View successful!'

        return HttpResponse(response_data)

def checkReadTenantWarning(request,id_warn):
    if request.method == 'POST':
        for p in Payment_Warning.objects.all():
            if p.id == id_warn:
                p.checkReadTenant = True
                p.save()
        response_data = {}
        response_data['result'] = 'View successful!'

        return HttpResponse(response_data)

def deletePopUpDuePayment(request):
    request.session['duePayments'] =  False
    return redirect('profile')

@login_required(login_url='login_view')
def reasons(request, agreement_id):
    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)
    try:
        lord = Landlord.objects.get(lord_user=a_user)
        agreement = Agreement.objects.get(pk = agreement_id)
    except:
        return redirect('index')
    if agreement.landlord != lord:
        return redirect('index')
    
    context  = {
        "agreement": agreement,
    }


    if request.method == 'POST':
        cause_objList = []

        data = request.POST
        causes_list = data.getlist('cause')
        new_incidence = Incidence()
        new_incidence.agreement = agreement
        new_incidence.filing_time = (date.today())

        new_incidence.description = data.get("description")
        if data.get("buttonPressed") == 'onlyIncidence':
            new_incidence.grouds_for_termination = 0
        
        else:
            new_incidence.grouds_for_termination = 1
            agreement.status = 0
            agreement.save()
        new_incidence.save()

        for cause in causes_list:
            cause_obj = Cause.objects.get(pk = int(cause))
            cause_objList.append(cause_obj)

        #new_incidence.causes.add(*cause_objList)
        new_incidence.causes.add(*cause_objList)
        new_incidence.save()    


        return render(request, "mainApp/reasons.html", context)

    return render(request, "mainApp/reasons.html", context)
    
def receipts(request):
    context={}

    if request.method == 'POST':
        agreement=request.POST['agreement_id']

        list_invoices = Invoice.objects.filter(agreement_id = agreement)

        fullList = []
        for i in list_invoices:
            try:
                receipt = Receipt.objects.get(invoice_id=i.id)
                fullList.append([i, receipt])
            except:
                pass
        context={
            'fullList': fullList,
        }
 
    return render(request, "mainApp/receipts.html", context)

def get_receipt_pdf(request):
    if request.method == 'POST':

        receipt_id=request.POST['receipt_id']

        if receipt_id != None:
            total = 0

            receipt = Receipt.objects.get(id=receipt_id)
            invoice = Invoice.objects.get(id=receipt.invoice_id)
            if (invoice.agreement_id == None):
                ag = Agreement_Request.objects.get(id=invoice.agreement_request_id)
            else:
                ag = Agreement.objects.get(id=invoice.agreement_id)
            tenant = Tenant.objects.get(id=ag.tenant_id)
            tenant_app = App_user.objects.get(user_id=tenant.ten_user_id)
            tenant_user = User.objects.get(id=tenant_app.user_id)
            list_invoice_line = Invoice_Line.objects.filter(invoice_id = invoice.id)

            for line in list_invoice_line:
                total += line.amount

            data = {
                'today': invoice.timestamp, 
                'customer_name': str(tenant_user.first_name) + " " + str(tenant_user.last_name),
                'order_id': receipt.id,
                'list_lines': list_invoice_line,
                'total_amount': total,
            }
            pdf = render_to_pdf('mainApp/receiptPDF.html', data)
            return HttpResponse(pdf, content_type='application/pdf')

def review(request):
    if request.method == 'POST':

        property_id = 1
        lord_id = 1

        conservation=request.POST['starsInput-1']
        landlord=request.POST['starsInput-2']
        services=request.POST['starsInput-3']
        access=request.POST['starsInput-4']
        neighbours=request.POST['starsInput-5']
        tenants=request.POST['starsInput-6']
        
        try:
            review = PropertyReview.objects.get(property_id = property_id)
        except:
            review = PropertyReview(
                property = Property.objects.get(id= property_id),
                num_reviews = 1,
                conservation = conservation,
                services = services,
                access = access, 
                neighbours = neighbours,
                tenants = tenants,
            )
            review.save()
            return render(request,'mainApp/profile.html', {})
        
        review.conservation = (review.conservation*review.num_reviews + int(conservation)) / (review.num_reviews + 1)
        review.services = (review.services*review.num_reviews + int(services)) / (review.num_reviews + 1)
        review.access = (review.access*review.num_reviews + int(access)) / (review.num_reviews + 1)
        review.neighbours = (review.neighbours*review.num_reviews + int(neighbours)) / (review.num_reviews + 1)
        review.tenants = (review.tenants*review.num_reviews + int(tenants)) / (review.num_reviews + 1)
        review.num_reviews = review.num_reviews + 1
        review.save()
        
        lord = Landlord.objects.get(id = lord_id)
        lord.lord_review = (lord.lord_review*lord.lord_review_num + int(landlord)) / (lord.lord_review_num + 1)
        lord.lord_review_num = lord.lord_review_num + 1
        lord.save()

    return render(request,'mainApp/reviewProperty.html', {})

def profileTenant(request,ten_id):
    tenant_user = User.objects.get(id=ten_id)
    tenant_app_user = App_user.objects.get(id=ten_id)

    context={"tenant_user":tenant_user, "tenant_app_user":tenant_app_user}
    return render(request, "mainApp/profileTenant.html", context)

def profileLandlord(request,lan_id):
    landlord_user = User.objects.get(id=lan_id)
    landlord_app_user = App_user.objects.get(id=lan_id)

    context={"landlord_user":landlord_user, "landlord_app_user":landlord_app_user}
    return render(request, "mainApp/profileLandlord.html", context)
