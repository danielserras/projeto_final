from django.shortcuts import render, redirect
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
from django.forms.models import model_to_dict
from django.db import connection
from decouple import config
from geopy.geocoders import MapBox
from copy import deepcopy
import time
import json
#tirar debug_mode no fim do proj
#tirar test_mode do paypal no fim

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('index') #placeholder, alterem depois
        else:
            messages.info(request, 'Username ou password incorretos')
            request.session['popUp'] =  False

            context = {}
            return render(request, 'mainApp/login.html', context) #placeholder
    context = {}
    return render(request,'mainApp/login.html', context) #placeholder

@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('login_view')


def register_view(request):
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
            return redirect('login_view') #placeholder, alterem depois   

    context = {'form':form, 'errors':form.errors} #, 'pform':pform
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


    if request.user.is_active:

        if request.method == 'POST':

            form_list = []
            bed_form = ''
            bath_form = ''
            kitchen_form = ''
            live_form = ''
            listing_form = ''

            prop_form = PropertyForm(data=request.POST)
            form_list.append(prop_form)

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
                form_list.append(listing_form)


            

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
                        
                
                    elif f == listing_form:
                        print(f)
                        if f.is_valid():

                            prop_album = ImageAlbum(name=f.cleaned_data.get('title'))
                            prop_album.save()

                            save_property(request)

                            listing_obj = Listing(
                                listing_type = f.cleaned_data.get('listing_type'),
                                allowed_gender = f.cleaned_data.get('allowed_gender'),
                                monthly_payment =  f.cleaned_data.get('monthly_payment'),
                                availability_starts =  f.cleaned_data.get('availability_starts'),
                                availability_ending =  f.cleaned_data.get('availability_ending'),
                                title =  f.cleaned_data.get('title'),
                                description =  f.cleaned_data.get('description'),
                                security_deposit =  f.cleaned_data.get('security_deposit'),
                                max_capacity =  f.cleaned_data.get('max_capacity'),
                                album = prop_album
                            )
                            listing_obj.save()

                                
                            assoc_prop = Property.objects.get(id=request.session['prop_id'])
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

                            del request.session['prop_serial']

                            if f.cleaned_data.get('listing_type') == 'Apartment' or f.cleaned_data.get('listing_type') == 'House':
                                apart_obj = Property_listing(main_listing = main_listing, associated_property = assoc_prop)
                                apart_obj.save()

                                context = {'imgformset': imgformset}
                                return redirect('index')
                                

                            elif f.cleaned_data.get('listing_type') == 'Bedroom' or f.cleaned_data.get('listing_type') == 'Residency' or f.cleaned_data.get('listing_type') == 'Studio':
                                room_obj = Room_listing(
                                    main_listing = main_listing,
                                    associated_room = Bedroom.objects.get(associated_property = assoc_prop))
                                room_obj.save()
                                
                                context = {'imgformset': imgformset}
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
def startsAgreement(request):

    if request.method == 'POST':
        pass
        #criar o agreement
        #efetuar o pagamento
        #apagar o listing
        #active/inactive no listing de modo a reutilizar
        
    else:

        #return render(request, "mainApp/startsAgreementTenent.html", {})
        return render(request, "mainApp/sendAgreementLandlord.html", {})

@login_required(login_url='login_view')
def create_request(request):

    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    try:
        lord = Landlord.objects.get(lord_user=a_user)
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

def property_edit_view(request, property_id):
    current_user = request.user
    a_user = App_user.objects.get(user_id=current_user)

    try:
        lord = Landlord.objects.get(lord_user=a_user)
    except:
        return redirect('index')

    property_object = Property.objects.get(id=property_id)
    bedrooms = list(Bedroom.objects.filter(associated_property=property_object))
    bathrooms = list(Bathroom.objects.filter(associated_property=property_object))
    kitchens = list(Kitchen.objects.filter(associated_property=property_object))
    livingrooms = list(Livingroom.objects.filter(associated_property=property_object))

    request.session["property_id"] = json.dumps(property_object.id)

    if request.method == 'POST':
        f = PropertyForm(data=request.POST)
        if f.is_valid():                
            prop_serial = json.dumps(f.cleaned_data)
            request.session['prop_serial'] = prop_serial

            context = {"bedrooms":bedrooms}
            
            return render(request,'mainApp/editBedrooms.html',context)
    else:
        context={"property":property_object}
        return render(request, "mainApp/editProperty.html", context)



def listing_edit_view(request, property_id):
    return render(request, "mainApp/listingEdit.html", {})

def notificationsLandlord(response):
    return render(response, "mainApp/notificationsLandlord.html", {})

def notifications3(response):
    return render(response, "mainApp/notifications3.html", {})


def search(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():

            geolocator = MapBox(config('MAPBOX_KEY'), scheme=None, user_agent=None, domain='api.mapbox.com')
                    
            location = geolocator.geocode(form.cleaned_data.get('location'))

            querySelect = 'SELECT l.monthly_payment, l.title, p.address, p.latitude, p.longitude'
            queryFrom = ' FROM mainApp_listing AS l, mainApp_property as p'
            queryWhere = " WHERE (acos(sin(p.latitude * 0.0175) * sin(38.7057409 * 0.0175) \
                            + cos(p.latitude * 0.0175) * cos(38.7057409 * 0.0175) *    \
                                cos((-9.16016118661616 * 0.0175) - (p.longitude * 0.0175))\
                            ) * 6371 <='" + str(form.cleaned_data.get('radius')) + "')"
            
            '''
                SELECT * FROM mainApp_property p 
                WHERE (
                        acos(sin(p.latitude * 0.0175) * sin(38.7057409 * 0.0175) 
                            + cos(p.latitude * 0.0175) * cos(38.7057409 * 0.0175) *    
                                cos((-9.16016118661616 * 0.0175) - (p.longitude * 0.0175))
                            ) * 6371 <= 23
                    )
            '''

            cursor = connection.cursor()
            
            #Checks if the price is within range
            queryWhere += " AND l.monthly_payment BETWEEN '" + form.cleaned_data.get('minPrice') + "' AND '" + form.cleaned_data.get('maxPrice') + "'"

            #Number of tenants is filled
            if any(form.cleaned_data.get('num_tenants') == x for x in ('1','2','3','4')):
                queryWhere += " AND l.max_capacity = '" + form.cleaned_data.get('num_tenants') + "'"
            
            #Date in is filled
            if form.cleaned_data.get('date_in') is not None:
                queryWhere += " AND '" + str(form.cleaned_data.get('date_in')) + "' >= l.availability_starts"
            
            #Date out is filled
            if form.cleaned_data.get('date_out') is not None:
                queryWhere += " AND '" + str(form.cleaned_data.get('date_out')) + "' <= l.availability_ending"

            #Number of bedrooms is filled
            if any(form.cleaned_data.get('num_bedrooms') == x for x in ('1','2','3','4')):
                queryWhere += " AND p.bedrooms_num = '" + form.cleaned_data.get('num_bedrooms') + "'"
            
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

                
                #print(querySelect + queryFromProperty + queryWhereProperty)
                #print(querySelect + queryFromRoom+ queryWhereRoom)

                cursor.execute(querySelect + queryFromProperty + queryWhereProperty)
                row_property = cursor.fetchall()

                cursor.execute(querySelect + queryFromRoom+ queryWhereRoom)
                row_room = cursor.fetchall()

                row = row_property + row_room
        print(row)
    return render(request, "mainApp/search.html", {})


def notificationsTenent(request):


    return render(request, "mainApp/notificationsTenent.html", {})

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
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

    app_user = App_user.objects.get(user=request.user)
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
    }
    return render(request, "mainApp/listingPage.html", context)

def countRoomDetails(rooms):
     
    num_details = 0
    for room in rooms:
        for k, v in model_to_dict(room).items():
            if v == True and isinstance(v, bool):
                num_details+=1
    
    return num_details