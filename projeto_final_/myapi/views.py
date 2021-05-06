import json
from django.shortcuts import render
from django.forms.models import model_to_dict

from rest_framework.response import Response

from rest_framework.decorators import permission_classes

from decouple import config

import mainApp

from rest_framework import viewsets, status, generics, permissions

from rest_framework.response import Response

from rest_framework.decorators import api_view

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import *

from mainApp.models import *

from django.contrib.auth import login

from knox.views import LoginView 

from rest_framework.views import APIView

from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, login, logout

from django.shortcuts import get_object_or_404

from geopy.geocoders import MapBox


#Funcoes acessorias

def response_maker(status, code, data, message):
    """
    Devolve um objeto response com um body em json e um codigo de status
    Status str, 'success' ou 'error'
    code int, codigo http de resposta dependendo do metodo e do resultado
    data dict, corpo de resposta da mensagem quando aplicavel
    message str, mensagem adicional de resposta quando aplicavel
    """
    body = {"status" : status, "code" : code, "data" : data, "message" : message}
    
    return Response(body, status=code)



# Create your views here.


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return response_maker("success", 200, None, "Utilizador registado.")

class LoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(request.data)
        print(request.data['username'])
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            return response_maker("success", 200, None, "Login realizado")
        else:
            return response_maker("error", 401, None, "Login falhado")

class getAuthToken(LoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            print(token[0])
            return response_maker("success", 200, {"authToken": str(token[0])}, None)
        else:
            return response_maker("error", 401, None, "password/username combination did not match any user")


#RF-9 
class agreementRequestAcceptAPI(generics.GenericAPIView):
    """Accept or refuse agreement request"""
    serializer_class = agreementRequestSerializer

    def put(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            agreement = serializer.save()
            return response_maker("success", 200, None, "Agreement request aceite.")
        except:
            return response_maker("error", 401, None, "Algo correu mal.")


#RF-18
class agreementRequestAPI(generics.GenericAPIView):
    serializer_class = createAgreementRequestSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            agreement_request = serializer.save()
            # return Response({
            # "user": App_userSerializer(user, context=self.get_serializer_context()).data,
            # })
            return response_maker("success", 200, None, "Criação do Agreement request feita.")
        except:
            return response_maker("error", 401, None, "Criação do Agreement request falhou.")


#um URI para adicionar propriedade, outro URI para listar Propriedade, outro URI por divisao (quarto, sala, sala de estar, casa de banho cozinha)
class Property(APIView):
    geolocator = MapBox(config('MAPBOX_KEY'), scheme=None, user_agent=None, domain='api.mapbox.com')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def post(self, request, format=None):
        user = request.user
        print(user)
        #token = (request.META["HTTP_AUTHORIZATION"].split("Token ")[1])
        #user = Token.objects.get(key=token).user
        appUser = App_user.objects.get(user = user)
        landLord = Landlord.objects.filter(lord_user = appUser)
        if not landLord:
            return response_maker("error", 405, None, "O tipo de utilizador não permite criação de propriedades")
            print(landLord)
        else:
            try:
                data = request.data
                location = self.geolocator.geocode(data["address"])
                dictToSerialize = {
                    "landlord": landLord[0].pk,
                    "address": data["address"],
                    "floor_area": data["floor_area"],
                    "garden": data["garden"],
                    "garage": data["garage"],
                    "street_parking": data["street_parking"],
                    "internet": data["internet"],
                    "electricity": data["electricity"],
                    "water": data["water"],
                    "gas": data["gas"],
                    "pets": data["pets"],
                    "overnight_visits": data["overnight_visits"],
                    "cleaning_services": data["cleaning_services"],
                    "smoke": data["smoke"],
                    "latitude": location.latitude,
                    "longitude": location.longitude, 
                    "bedrooms_num": data["bedrooms_num"],
                    "listing_type": data["listing_type"]
                }
            except:
                return response_maker("error", 409, None, "Missing necessary fields")
            serializer = PropertySerializer(data=dictToSerialize)
            serializer.is_valid(raise_exception=True)
            newProperty = serializer.save()
            responseData = serializer.data
            responseData["id"] = newProperty.id
            return response_maker("success", 201, serializer.data, "New Property created w/ id %d"%newProperty.id)

    def get(self, request, pk):
        property_matching_id = mainApp.models.Property.objects.filter(pk=pk)
        
        if not property_matching_id:
            return response_maker("error", 404, None, "No property matching id %d"%pk)
        else:
            responseData = model_to_dict(property_matching_id[0])
            return response_maker("success", 200, responseData, None)
        



class SearchListing(APIView):
    def post(self, request):
        pass
        

class imageTest(generics.GenericAPIView):
    serializer_class = imageTestSerializer
    def post(self, request):
        print(request.data)
        return response_maker("success", 200, None, "Criação do Agreement request criado.")
        

#RF-4
class UserAPI(APIView):
    """Show specific user, Delete user from database and update specific info about the user"""

    def get(self, request, pk):
        user = User.objects.get(id = pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, id=pk)
        data = request.data 

        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.password = data.get('password', user.password)
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data)

    #falta poder alterar info do lado do app_user
    def delete(self, request, pk):
        
        user = get_object_or_404(User, id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

