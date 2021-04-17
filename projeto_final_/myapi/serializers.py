from rest_framework import serializers

from mainApp.models import *

from django.utils import timezone


class App_userSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    
class TenantSerializer(serializers.HyperlinkedModelSerializer):
    ten_user = App_userSerializer(many=False)
    class Meta:
        model = Tenant
        fields = ('id', 'ten_user')
    
class LandlordSerializer(serializers.HyperlinkedModelSerializer):
    lord_user = App_userSerializer(many=False)
    class Meta:
        model = Landlord
        fields = ('id', 'lord_type', 'lord_user')


# Register Serializer

#FALTA ACRESCENTAR OS CAMPOS PHONENUMBER E DATANASCIMENTO e definir se é tenant ou landlord
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class agreementRequestSerializer(serializers.ModelSerializer): 
    idNumber = serializers.IntegerField()
    class Meta:
        model = Agreement_Request

        fields = ('idNumber', 'accepted')
    
    def create(self, validated_data):
        idN = validated_data['idNumber']
        accepted = validated_data['accepted']
        #print(Agreement_Request.objects.get(id=idN).accepted)
        agreement_request = Agreement_Request.objects.get(id=idN)
        agreement_request.accepted = accepted
        #print(agreement_request.accepted)
        agreement_request.save()
        return agreement_request

class createAgreementRequestSerializer(serializers.ModelSerializer):
    tenant_id = serializers.IntegerField() #id
    landlord_id = serializers.IntegerField() #id
    associated_room_listing_id = serializers.IntegerField() #id
    associated_property_listing_id = serializers.IntegerField() #id

    class Meta:
        model = Agreement_Request
        fields = ('id', 'startsDate', 'endDate', 'message', 'tenant_id', 'landlord_id', 'associated_property_listing_id', 'associated_room_listing_id')
        

    def create(self, validated_data):
        if validated_data['associated_room_listing_id'] == 0:
            validated_data.pop('associated_room_listing_id')
            dateNow = timezone.now()
            validated_data['dateOfRequest'] = dateNow
            print(validated_data['dateOfRequest'])
            agreement_request = Agreement_Request.objects.create(**validated_data)

            return agreement_request
        else:
            validated_data.pop('associated_property_listing_id')
            dateNow = timezone.now()
            validated_data['dateOfRequest'] = dateNow
            print(validated_data['dateOfRequest'])
            agreement_request = Agreement_Request.objects.create(**validated_data)

            return agreement_request
    
class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

   
