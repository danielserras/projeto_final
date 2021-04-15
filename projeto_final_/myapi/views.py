import json
from django.shortcuts import render

from rest_framework.response import Response

from rest_framework import viewsets, status, generics, permissions

from rest_framework.response import Response

from rest_framework.decorators import api_view

from .serializers import *

from mainApp.models import * 

from django.contrib.auth import login

from knox.views import LoginView 
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

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
        return Response({
        "user": App_userSerializer(user, context=self.get_serializer_context()).data,
        })

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

class IntroduceProperty(APIView):
    def post(self, request, format=None):
        content = {
            'user': str(request.user),  
            'auth': str(request.auth), 
        }
        return Response(content)


#RF-9 
class receiveNotificationAPI(generics.GenericAPIView):
    """Accept or refuse agreement request"""
    serializer_class = agreementRequestSerializer

    def put(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            agreement = serializer.save()
            return response_maker("success", 200, None, "Alteração realizada")
        except:
            return response_maker("error", 401, None, "Alteração falhada")


#RF-18
class agreementRequestAPI(generics.GenericAPIView):
    serializer_class = createAgreementRequestSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            print("ola1")
            serializer.is_valid(raise_exception=True)
            print("ola2")
            agreement_request = serializer.save()
            print("ola3")
            # return Response({
            # "user": App_userSerializer(user, context=self.get_serializer_context()).data,
            # })
            return response_maker("success", 200, None, "Criação do Agreement request criado.")
        except:
            return response_maker("error", 401, None, "Criação do Agreement request falhou.")

# @api_view(['POST',])
# def registration_view(request):
#     if request.method == 'POST':
#         serializer = RegisterSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = "Successfully registered a new user"
#             data['username'] = user.username
#             data['email'] = user.email
#             data['first_name'] = user.first_name
#             data['last_name'] = user.last_name
#         else:
#             data = serializer.errors
#         return Response(data)

