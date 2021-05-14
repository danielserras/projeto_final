from django.conf import settings
from .models import *
from .views import *
from django.contrib.auth.decorators import login_required


def numUnreadNotifations(request):
    if request.user.is_authenticated:
        current_user_ = request.user
        a_user = App_user.objects.get(user_id=current_user_)
        numUnreadNotifications = 0 
        landlord = False
        tenant = False
        try:
            landlord = Landlord.objects.get(lord_user=a_user)
        except:
            tenant = Tenant.objects.get(ten_user=a_user)
        if landlord:
            agreements_req= Agreement_Request.objects.filter(landlord=landlord)
            refunds = Refund.objects.filter(landlord=landlord)
            for a in agreements_req:
                if a.checkReadLandlord !=True:
                    numUnreadNotifications += 1
            for r in refunds:
                if r.checkReadLandlord !=True:
                    numUnreadNotifications += 1
        else:
            ag_req = Agreement_Request.objects.filter(tenant=tenant)
            agreements = Agreement.objects.filter(tenant=tenant)

            invoicesList = []
            for a in agreements:
                inv = Invoice.objects.filter(agreement=a)
                invoicesList.append(inv)

            paywList = []   
            for a in agreements: 
                payw = Payment_Warning.objects.filter(agreement=a)
                paywList.append(payw)

            for a in ag_req:
                if a.checkReadTenant !=True:
                    numUnreadNotifications += 1
            for i in invoicesList:
                for j in i:
                    if j.checkReadTenant !=True:
                        numUnreadNotifications += 1
            for p in paywList:
                for j in p:
                    if j.checkReadTenant !=True:
                        numUnreadNotifications += 1
        
        return {"numUnreadNotifications":numUnreadNotifications}
    else:
        return {"numUnreadNotifications":None}
    