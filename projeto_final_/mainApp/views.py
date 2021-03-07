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
import time
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
    return redirect('index')


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

@login_required(login_url='/')
def introduce_property_view (request):

    if request.method == 'POST':

        current_user = request.user
        a_user = App_user.objects.get(user_id=current_user)
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
                        prop_object = Property(
                            landlord = Landlord.objects.get(lord_user=a_user),
                            address = f.cleaned_data.get('address'),
                            floor_area = f.cleaned_data.get('floor_area'),
                            garden = f.cleaned_data.get('garden'),
                            garage = f.cleaned_data.get('garage'),
                            street_parking = f.cleaned_data.get('street_parking'),
                            internet = f.cleaned_data.get('internet'),
                            electricity = f.cleaned_data.get('electricity'),
                            water = f.cleaned_data.get('water'),
                            gas = f.cleaned_data.get('gas'),
                            pets = f.cleaned_data.get('pets'),
                            overnight_visits = f.cleaned_data.get('overnight_visits'),
                            cleaning_services = f.cleaned_data.get('cleaning_services'),
                            smoke = f.cleaned_data.get('smoke')
                        )
                        prop_object.save()
                        bed_formset = BedroomFormSet(queryset=Bedroom.objects.none())
                        bed_formset.extra = int(f.cleaned_data.get('bedrooms_num'))
                        
                        request.session['bedrooms_num'] =  f.cleaned_data.get('bedrooms_num')
                        request.session['bathrooms_num'] =  f.cleaned_data.get('bathrooms_num')
                        request.session['kitchens_num'] =  f.cleaned_data.get('kitchens_num')
                        request.session['livingrooms_num'] =  f.cleaned_data.get('livingrooms_num')
                        request.session['prop_id'] = prop_object.id

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
                    for sub_form in f:

                        bath_object = Bathroom(
                            associated_property = Property.objects.get(id=int(request.session['prop_id'])),
                            toilet = sub_form.cleaned_data.get('toilet'),
                            sink = sub_form.cleaned_data.get('sink'),
                            shower = sub_form.cleaned_data.get('shower'),
                            b_window = sub_form.cleaned_data.get('b_window'),
                            bathtub = sub_form.cleaned_data.get('bathtub'),
                            bidet = sub_form.cleaned_data.get('bidet')
                        )
                        bath_object.save()

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
                    for sub_form in f:

                        kitchen_obj = Kitchen(
                            associated_property = Property.objects.get(id=int(request.session['prop_id'])),
                            oven = sub_form.cleaned_data.get("oven"),            
                            dish_washer = sub_form.cleaned_data.get("dish_washer"),  
                            k_window = sub_form.cleaned_data.get("k_window"),  
                            fridge = sub_form.cleaned_data.get("fridge"),  
                            freezer = sub_form.cleaned_data.get("freezer"),  
                            cooker = sub_form.cleaned_data.get("cooker"),  
                            dishes_cutlery = sub_form.cleaned_data.get("dishes_cutlery"),  
                            pans_pots = sub_form.cleaned_data.get("pans_pots"),  
                            dishwasher_machine = sub_form.cleaned_data.get("dishwasher_machine"),  
                            dryer = sub_form.cleaned_data.get("dryer"),
                            k_table = sub_form.cleaned_data.get("k_table"),
                            laundering_machine = sub_form.cleaned_data.get("laundering_machine"),
                            k_chairs = sub_form.cleaned_data.get("k_chairs"),
                            microwave = sub_form.cleaned_data.get("microwave"),
                            k_balcony = sub_form.cleaned_data.get("k_balcony")
                        )
                        kitchen_obj.save()

                    if request.session['livingrooms_num'] > 0:
                        live_formset = LivingroomFormSet(queryset=Livingroom.objects.none())

                        live_formset.extra = int(request.session['livingrooms_num'])
                        del request.session['kitchens_num']

                        context = {'live_formset': live_formset}
                        return render(request, 'mainApp/addLivingroom.html', context)
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
                    for sub_form in f:
                        
                        live_obj = Livingroom(
                            associated_property = Property.objects.get(id=int(request.session['prop_id'])),
                            l_chairs = sub_form.cleaned_data.get('l_chairs'),
                            l_sofa = sub_form.cleaned_data.get('l_sofa'),
                            l_sofa_bed = sub_form.cleaned_data.get('l_sofa_bed'),
                            l_window = sub_form.cleaned_data.get('l_window'),
                            l_table = sub_form.cleaned_data.get('l_table'),
                            l_balcony = sub_form.cleaned_data.get('l_balcony'),
                            l_desk = sub_form.cleaned_data.get('l_desk')
                        )
                        live_obj.save()

                    listing_form = ListingForm()

                    request.session['listing'] =  True
                    del request.session['livingrooms_num']

                    imgformset = ImgFormSet(queryset=Image.objects.none())
                    context = {'listing_form': listing_form, 'imgformset' : imgformset}

                    return render(request, 'mainApp/addListing.html', context)
                    
                
                elif f == bed_form:
                    print(f)
                    for sub_form in f:
                        
                        bed_obj = Bedroom(
                            associated_property = Property.objects.get(id=int(request.session['prop_id'])),
                            be_chairs = sub_form.cleaned_data.get('be_chairs'),
                            be_sofa = sub_form.cleaned_data.get('be_sofa'),
                            be_sofa_bed = sub_form.cleaned_data.get('be_sofa_bed'),
                            be_window = sub_form.cleaned_data.get('be_window'),
                            num_single_beds = sub_form.cleaned_data.get('num_single_beds'),
                            num_double_beds = sub_form.cleaned_data.get('num_double_beds'),
                            be_balcony = sub_form.cleaned_data.get('be_balcony'),
                            wardrobe = sub_form.cleaned_data.get('wardrobe'),
                            be_desk = sub_form.cleaned_data.get('be_desk'),
                            lock = sub_form.cleaned_data.get('lock'),
                            chest_of_drawers = sub_form.cleaned_data.get('chest_of_drawers'),
                            tv = sub_form.cleaned_data.get('tv'),
                            heater = sub_form.cleaned_data.get('heater'),
                            air_conditioning = sub_form.cleaned_data.get('air_conditioning'),
                            ensuite_bathroom = sub_form.cleaned_data.get('ensuite_bathroom'),
                            max_occupacity = sub_form.cleaned_data.get('max_occupacity'),
                        )
                        bed_obj.save()

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

                        
                        assoc_prop = Property.objects.get(id=int(request.session['prop_id']))
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

                        if f.cleaned_data.get('listing_type') == 'Apartment':
                            apart_obj = Property_listing(main_listing = main_listing, associated_property = assoc_prop)
                            apart_obj.save()

                            context = {'imgformset': imgformset}
                            return redirect('index')
                            

                        elif f.cleaned_data.get('listing_type') == 'Bedroom':
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


def index(response):
    return render(response, "mainApp/home.html", {})

def startsAgreement(response):

    if request.method == 'POST':
        pass
        #criar o agreement
        #efetuar o pagamento
        #apagar o listing
        #active/inactive no listing de modo a reutilizar
        
    else:

        return render(response, "mainApp/startsAgreementTenent.html", {})
    #return render(response, "mainApp/sendAgreementLandlord.html", {})


def create_request(request):

    if request.method == 'POST':
        ag_form = Agreement_Request_Form()
        #popular campos do form de antemao com info sobre a propriedade

        context = {'ag_form': ag_form}
        return render(request, 'mainApp/intent.html', context)
    
    else:
        #nao deve cair aqui
        return redirect('index')

        
def send_request(request):

    if request.method == 'POST':
        #inq ja preencheu tudo no form, falta criar agreement_request
        ag_form = Agreement_Request_Form(data=request.POST)
        if ag_form.is_valid():

            room_id = ag_form.cleaned_data.get('associated_room_listing')
            prop_id = ag_form.cleaned_data.get('associated_property_listing')
            tenant_id = ag_form.cleaned_data.get('tenant')
            landlord_id = ag_form.cleaned_data.get('landlord')
            start_date = ag_form.cleaned_data.get('startsDate')
            end_date = ag_form.cleaned_data.get('endDate')
            message = ag_form.cleaned_data.get('message')

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

    return redirect('home_page')


def profile(response):
    return render(response, "mainApp/profile.html", {})

def notifications2(response):
    return render(response, "mainApp/notifications2.html", {})

def notifications3(response):
    return render(response, "mainApp/notifications3.html", {})


def intent(response):
    return render(response, "mainApp/intent.html", {})

def search(request):
    form = CreateUserForm()
    if request.method == 'POST':
        print(form.errors)
        form = SearchForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('location'))
            print(form.cleaned_data.get('radius'))
            print(form.cleaned_data.get('type'))
            print(form.cleaned_data.get('num_tenants'))
            print(form.cleaned_data.get('num_bedrooms'))
            print(form.cleaned_data.get('date_in'))
            print(form.cleaned_data.get('date_out'))
            print(form.cleaned_data.get('minPrice'))
            print(form.cleaned_data.get('maxPrice'))

    return render(request, "mainApp/search.html", {})

""" def addListing(response):
    return render(response, "mainApp/addListing.html", {}) """

def notifications(response):
    return render(response, "mainApp/notifications.html", {})

def listing(response, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing_type = listing.listing_type
    bedrooms = []

    if listing_type == "Bedroom":
        associated_object = listing.r_main.associated_room #associated object is a Bedroom
        parent_property = associated_object.associated_property
        bedrooms.append(associated_object)

        request.session['room_listing'] = Room_listing.objects.filter(associated_room=associated_object)
    

    else:
        associated_object = listing.p_main.associated_property #associated object is a property
        parent_property = associated_object

        bedrooms = list(Bedroom.objects.filter(associated_property = parent_property))

        request.session['property_listing'] = Property_listing.objects.filter(associated_property=associated_object)
        
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

    app_user = App_user.objects.filter(user=request.user)
    tenant = Tenant.objects.filter(ten_user=app_user)

    request.session['tenant'] = tenant
    request.session['landlord'] = landlord

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
    }
    return render(response, "mainApp/listingPage.html", context)

def countRoomDetails(rooms):
     
    num_details = 0
    for room in rooms:
        for k, v in model_to_dict(room).items():
            if v == True and isinstance(v, bool):
                num_details+=1
    
    return num_details