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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('home_page') #placeholder, alterem depois
        else:
            messages.info(request, 'Username ou password incorretos')
            return redirect('index') #placeholder
    context = {}
    return render(request,'mainApp/login.html', context) #placeholder


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
                app_user_object.tenant_set.create(ten_user=app_user_object)
            else:
                app_user_object.landlord_set.create(lord_user=app_user_object)
            #pform = p_form.save(commit=False)
            #pform.user = user
            #pform.save()
            user_nameStr = form.cleaned_data.get('username')
            user_first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'Utilizador ' + user_nameStr + ' criado!')

            return redirect('search') #placeholder, alterem depois   

    context = {'form':form} #, 'pform':pform
    return render(request, 'mainApp/register.html', context)

def introduce_property_view (request):

    if request.method == 'POST':
        a_user = App_user.objects.get(user_id=request.user)

        prop_form = PropertyForm(data=request.POST)
        bath_form = BathroomFormSet(data=request.POST)
        kitchen_form = KitchenFormSet(data=request.POST)
        live_form = LivingroomFormSet(data=request.POST)
        bed_form = BedroomFormSet(data=request.POST)
        listing_form = ListingForm(data=request.POST)

        form_list = [prop_form, bath_form, kitchen_form, live_form, bed_form, listing_form]

        for f in form_list:
            if f.is_bound:

                if f == prop_form:
                    if f.is_valid():
                        prop_object = Property(
                            property_type = f.cleaned_data.get('property_type'),
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

                elif f == bath_form:
                    for sub_form in f:
                        bath_object = Bathroom(
                            associated_property = prop_object,
                            toilet = sub_form.cleaned_data.get('toilet'),
                            sink = sub_form.cleaned_data.get('sink'),
                            shower = sub_form.cleaned_data.get('shower'),
                            window = sub_form.cleaned_data.get('window'),
                            bathtub = sub_form.cleaned_data.get('bathtub'),
                            private_or_shared = sub_form.cleaned_data.get('private_or_shared')
                        )
                        bath_object.save()


                elif f == kitchen_form:
                    for sub_form in f:
                        kitchen_obj = Kitchen(
                            associated_property = prop_object,
                            oven = sub_form.cleaned_data.get("oven"),            
                            dish_washer = sub_form.cleaned_data.get("dish_washer"),  
                            window = sub_form.cleaned_data.get("window"),  
                            fridge = sub_form.cleaned_data.get("fridge"),  
                            freezer = sub_form.cleaned_data.get("freezer"),  
                            cooker = sub_form.cleaned_data.get("cooker"),  
                            dishes_cutlery = sub_form.cleaned_data.get("dishes_cutlery"),  
                            pans_pots = sub_form.cleaned_data.get("pans_pots"),  
                            washing_machine = sub_form.cleaned_data.get("washing_machine"),  
                            dryer = sub_form.cleaned_data.get("dryer"),
                        )
                        kitchen_obj.save()

                elif f == live_form:
                    for sub_form in f:
                        live_obj = Livingroom(
                            associated_property = prop_object,
                            chairs = sub_form.cleaned_data.get('chairs'),
                            sofa = sub_form.cleaned_data.get('sofa'),
                            sofa_bed = sub_form.cleaned_data.get('sofa_bed'),
                            window = sub_form.cleaned_data.get('window'),
                            table = sub_form.cleaned_data.get('table'),
                            balcony = sub_form.cleaned_data.get('balcony')
                        )
                        live_obj.save()

                elif f == bed_form:
                    for sub_form in f:
                        bed_obj = Bedroom(
                            associated_property = prop_object,
                            chairs = sub_form.cleaned_data.get('chairs'),
                            sofa = sub_form.cleaned_data.get('sofa'),
                            sofa_bed = sub_form.cleaned_data.get('sofa_bed'),
                            window = sub_form.cleaned_data.get('window'),
                            num_single_beds = sub_form.cleaned_data.get('num_single_beds'),
                            num_double_beds = sub_form.cleaned_data.get('num_double_beds'),
                            balcony = sub_form.cleaned_data.get('balcony'),
                            wardrobe = sub_form.cleaned_data.get('wardrobe'),
                            desk = sub_form.cleaned_data.get('desk'),
                            chest_of_drawers = sub_form.cleaned_data.get('chest_of_drawers'),
                            tv = sub_form.cleaned_data.get('tv'),
                            heater = sub_form.cleaned_data.get('heater'),
                            air_conditioning = sub_form.cleaned_data.get('air_conditioning'),
                            ensuite_bathroom = sub_form.cleaned_data.get('ensuite_bathroom'),
                        )
                        bed_obj.save()
                
                elif f == listing_form:
                    if f.is_valid():
                        listing_obj = Listing(
                            allowed_gender = f.cleaned_data.get('allowed_gender'),
                            monthly_payment =  f.cleaned_data.get('monthly_payment'),
                            availabilityStarts =  f.cleaned_data.get('availabilityStarts'),
                            availabilityEnds =  f.cleaned_data.get('availabilityEnds'),
                            title =  f.cleaned_data.get('title'),
                            description =  f.cleaned_data.get('description'),
                            security_deposit =  f.cleaned_data.get('security_deposit'),
                            max_capacity =  f.cleaned_data.get('max_capacity')
                        )
                        listing_obj.save()

        return redirect('home')     #PLACEHOLDER
                        
    else:
        prop_form = PropertyForm(queryset=Property.objects.none())
        bath_formset = BathroomFormSet(queryset=Bathroom.objects.none())
        kitchen_formset = KitchenFormSet(queryset=Kitchen.objects.none())
        live_formset = LivingroomFormSet(queryset=Livingroom.objects.none())
        bed_formset = BedroomFormSet(queryset=Bedroom.objects.none())
        listing_form = ListingForm(queryset=Listing.objects.none())

        return render_to_response({
            'property_form': prop_form, 
            'bath_formset': bath_formset,
            'kitchen_formset': kitchen_formset,
            'live_formset': live_formset,
            'bed_formset': bed_formset,
            'listing_form': listing_form
            })

def index(response):
    return render(response, "mainApp/home.html", {})

def startsAgreement(response):
    return render(response, "mainApp/startsAgreementTenent.html", {})
    #return render(response, "mainApp/sendAgreementLandlord.html", {})

def profile(response):
    return render(response, "mainApp/profile.html", {})

def search(response):
    return render(response, "mainApp/search.html", {})

def addListing(response):
    return render(response, "mainApp/addListing.html", {})