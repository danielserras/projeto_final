from django.shortcuts import render

from rest_framework import viewsets, status, generics, permissions

from rest_framework.response import Response

from rest_framework.decorators import api_view

from .serializers import *

from mainApp.models import * 

from django.contrib.auth import login

from knox.views import LoginView 

from django.contrib.auth import authenticate, login, logout


# Create your views here.

class registerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = App_userSerializer



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
            return Response({
                "Login realizado"
                })
        else:
            return Response({
            "Login falhado"
            })

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

