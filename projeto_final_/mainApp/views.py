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
                ten = Tenant(ten_user=app_user_object)
                ten.save()
            else:
                lord = Landlord(lord_user=app_user_object)
                lord.save()
                
            user_nameStr = form.cleaned_data.get('username')
            user_first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'Utilizador ' + user_nameStr + ' criado!')

            return redirect('search') #placeholder, alterem depois   

    context = {'form':form} #, 'pform':pform
    return render(request, 'mainApp/register.html', context)

def introduce_property_view (request):

    if request.method == 'POST':

        test_user = User.objects.filter(id=1)
        a_user = App_user.objects.get(user_id__in=test_user)
        
        prop_form = PropertyForm(data=request.POST)
        bed_form = BedroomFormSet(data=request.POST)
        bath_form = BathroomFormSet(data=request.POST)
        kitchen_form = KitchenFormSet(data=request.POST)
        live_form = LivingroomFormSet(data=request.POST)
        listing_form = ListingForm(data=request.POST)


        form_list = [prop_form, bed_form, bath_form, kitchen_form, live_form, listing_form]

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
                        bed_formset = BedroomFormSet(queryset=Bedroom.objects.none(), initial=[{'prop_id': prop_object.id,}])

                        bed_formset.extra = int(f.cleaned_data.get('bedrooms_num'))
                        context = {'property_form': prop_form, 'bed_formset': bed_formset}
                        return render(
                            request,
                            'mainApp/addBedroom.html',
                            context)

                elif f == bath_form:
                    #print(f)
                    for sub_form in f:
                        bath_object = Bathroom(
                            associated_property = prop_object,
                            toilet = sub_form.cleaned_data.get('toilet'),
                            sink = sub_form.cleaned_data.get('sink'),
                            shower = sub_form.cleaned_data.get('shower'),
                            b_window = sub_form.cleaned_data.get('b_window'),
                            bathtub = sub_form.cleaned_data.get('bathtub'),
                            bidet = sub_form.cleaned_data.get('bidet')
                        )
                        bath_object.save()
                        """kitchen_formset = KitchenFormSet(queryset=Kitchen.objects.none())
                        kitchen_formset.extra = int(f.cleaned_data.get('kitchens_num'))
                        kitchen_formset[0].prop_id = prop_object.id
                        
                        context = {'property_form': prop_form, 'kitchen_formset': kitchen_formset}
                        return render(
                            request,
                            'mainApp/addKitchen.html',
                            context)"""


                elif f == kitchen_form:
                    #print(f)
                    for sub_form in f:
                        #print(sub_form.)
                        kitchen_obj = Kitchen(
                            associated_property = prop_object,
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

                elif f == live_form:
                    #print(f)
                    for sub_form in f:
                        live_obj = Livingroom(
                            associated_property = prop_object,
                            l_chairs = sub_form.cleaned_data.get('l_chairs'),
                            l_sofa = sub_form.cleaned_data.get('l_sofa'),
                            l_sofa_bed = sub_form.cleaned_data.get('l_sofa_bed'),
                            l_window = sub_form.cleaned_data.get('l_window'),
                            l_table = sub_form.cleaned_data.get('l_table'),
                            l_balcony = sub_form.cleaned_data.get('l_balcony'),
                            l_desk = sub_form.cleaned_data.get('l_desk')
                        )
                        live_obj.save()
                
                elif f == bed_form:
                    print('entrou-----------------------------------')
                    for sub_form in f:
                        print(sub_form.initial)
                        bed_obj = Bedroom(
                            associated_property = Property.objects.get(id=sub_form.cleaned_data['prop_id']),
                            be_chairs = sub_form.cleaned_data.get('be_chairs'),
                            be_sofa = sub_form.cleaned_data.get('be_sofa'),
                            be_sofa_bed = sub_form.cleaned_data.get('be_sofa_bed'),
                            be_window = sub_form.cleaned_data.get('be_window'),
                            num_single_beds = sub_form.cleaned_data.get('num_single_beds'),
                            num_double_beds = sub_form.cleaned_data.get('num_double_beds'),
                            be_balcony = sub_form.cleaned_data.get('be_balcony'),
                            wardrobe = sub_form.cleaned_data.get('wardrobe'),
                            be_desk = sub_form.cleaned_data.get('be_desk'),
                            chest_of_drawers = sub_form.cleaned_data.get('chest_of_drawers'),
                            tv = sub_form.cleaned_data.get('tv'),
                            heater = sub_form.cleaned_data.get('heater'),
                            air_conditioning = sub_form.cleaned_data.get('air_conditioning'),
                            ensuite_bathroom = sub_form.cleaned_data.get('ensuite_bathroom'),
                            max_occupacity = sub_form.cleaned_data.get('max_occupacity'),
                        )
                        bed_obj.save()
                        bath_formset = BathroomFormSet(queryset=Bathroom.objects.none())
                        bath_formset.extra = int(f.cleaned_data.get('bathrooms_num'))
                        bath_formset[0].prop_id = prop_object.id

                        context = {'property_form': prop_form, 'bath_formset': bath_formset}
                        return render(
                            request,
                            'mainApp/addBathroom.html',
                            context)
                
                elif f == listing_form:
                    #print(f)
                    if f.is_valid():
                        listing_obj = Listing(
                            allowed_gender = f.cleaned_data.get('allowed_gender'),
                            monthly_payment =  f.cleaned_data.get('monthly_payment'),
                            availability_starts =  f.cleaned_data.get('availability_starts'),
                            availability_ending =  f.cleaned_data.get('availability_ending'),
                            title =  f.cleaned_data.get('title'),
                            description =  f.cleaned_data.get('description'),
                            security_deposit =  f.cleaned_data.get('security_deposit'),
                            max_capacity =  f.cleaned_data.get('max_capacity')
                        )
                        listing_obj.save()

        return redirect('home')     #PLACEHOLDER
                        
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

        """ return render(
        request,
        'mainApp/addListing.html',
        {'property_form': prop_form, 
        'bath_formset': bath_formset,
        'kitchen_formset': kitchen_formset,
        'live_formset': live_formset,
        'bed_formset': bed_formset,
        'listing_form': listing_form
        }) """

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
        #popular campos do form com info do search sobre a propriedade

        context = {'ag_form': ag_form}
        return render(request, 'mainApp/sendRequest.html', context)

        
def send_request(request):

    if request.method == 'POST':
        #inq ja preencheu tudo no form, falta criar agreement_request
        ag_form = Agreement_Request_Form(data=request.POST)
        if ag_form.is_valid():
            ag_form.save()
            return redirect('home_page')


def profile(response):
    return render(response, "mainApp/profile.html", {})

def search(response):
    return render(response, "mainApp/search.html", {})

""" def addListing(response):
    return render(response, "mainApp/addListing.html", {}) """

def notifications(response):
    return render(response, "mainApp/notifications.html", {})

def listing(response):
    return render(response, "mainApp/listingPage.html", {})
