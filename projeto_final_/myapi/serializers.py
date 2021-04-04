from rest_framework import serializers

from mainApp.models import *


class App_userSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',)

    
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
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ( 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.save()
        return user

    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
    

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
    

   
