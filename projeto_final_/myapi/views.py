from django.shortcuts import render

from rest_framework import viewsets, status

from rest_framework.response import Response

from rest_framework.decorators import api_view

from .serializers import *

from mainApp.models import * 

# Create your views here.

class registerViewSet(viewsets.ModelViewSet):
    print("ola")
    queryset = User.objects.all()
    serializer_class = App_userSerializer


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully registered a new user"
            data['username'] = user.username
            data['email'] = user.email
        else:
            data = serializer.errors
        return Response(data)
    