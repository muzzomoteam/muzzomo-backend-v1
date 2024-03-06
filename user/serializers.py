from django.contrib.auth.hashers import make_password
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django .contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes, force_str
from django.urls import reverse
from .utils import send_normal_email


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68,min_length = 6, write_only = True)
    password2 = serializers.CharField(max_length = 68,min_length = 6, write_only = True)
    
    class  Meta:
        model = User
        fields=['email', 'first_name', 'last_name', 'password','password2']
        
    def validate(self, attrs):
        password = attrs.get('password','')
        password2 = attrs.get('password2','')
        if password != password2:
            raise serializers.ValidationError('passwords do not match')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            password = validated_data.get('password'),

        )
        return user
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length = 255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255,read_only=True)
    access_token = serializers.CharField(max_length = 255, read_only = True)
    refresh_token = serializers.CharField(max_length = 255, read_only = True)
    
    class Meta:
        model = User
        fields=['email','password','full_name', 'refresh_token', 'access_token']
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request=self.context.get('request')
        user = authenticate(request, email = email, password = password)
        if not user:
            raise AuthenticationFailed('invalid credintials try again')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        user_tokens = user.tokens()
        
        return{
            'email':user.email,
            'full_name':user.get_full_name,
            'access_token' : str(user_tokens.get('access')),
            'refresh_token':str(user_tokens.get('refresh'))
        }
        
        
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    class  Meta:
       fields=['email']
       
    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email = email):
            user = User.objects.get(email = email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            site_domain=get_current_site(request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abslink=f"http://{site_domain}{relative_link}"
            email_body=f"Hi use the link below to reset your password \n {abslink}"
            data={
                'email_body':email_body,
                'email_subject':'Reset Your Password',
                'to_email':user.email
            }
            send_normal_email(data)
            
        return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6,write_only=True)
    confirm_password=serializers.CharField(max_length=100,min_length=6,write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)
    
    class Meta:
        fields=['password',
                'confirm_password',
                'uidb64',
                'token']
    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password=attrs.get('confirm_password')
            
            user_id = force_str(urlsafe_base64_encode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('reset link is invalid or has expired')
            if password != confirm_password:
                raise AuthenticationFailed("passwords do not match")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed('link is invalid or expired')

# ----------------------------

class CountrySerializer(serializers.ModelSerializer):
  class Meta:
    model = Country
    fields = ['id' , 'name']
class ProvinceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Province
    fields = ['id' , 'name' , 'country']
class CitySerializer(serializers.ModelSerializer):
  class Meta:
    model = City
    fields = ['id' , 'name' , 'province']
class AddressSerializer(serializers.ModelSerializer):
  city = CitySerializer()
  class Meta:
    model = Address
    fields = ['id' , 'street' , 'city']

class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id' , 'email' , 'first_name', 'last_name']

class ProfessionalSerializer(serializers.ModelSerializer):
  first_name = serializers.CharField(source = 'admin.first_name', read_only = True)
  last_name = serializers.CharField(source = 'admin.last_name', read_only = True)
  address_city = serializers.CharField(source = 'address.city.province' , read_only = True)

  class Meta:
    model = Professional
    fields = ['id' , 'admin' , 'license_number' , 'insurance_number' , 'service' , 'address','profile_image' , 'phone', 'first_name', 'last_name', 'address_city']

class SimpleUserSerializer(serializers.ModelSerializer):
  first_name = serializers.CharField(source = 'admin.first_name', read_only = True)
  last_name = serializers.CharField(source = 'admin.last_name', read_only = True)
  address_city = serializers.CharField(source = 'address.city.province' , read_only = True)
  provider_email = serializers.CharField(source = 'admin.email', read_only = True)

  class Meta:
    model = Provider
    fields = ['id' , 'admin','profile_image' , 'phone' , 'address', 'first_name', 'last_name', 'address_city', 'provider_email']

       
class ProfessionalRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ['id' , 'admin' , 'phone' ,'service' ,'address' , 'license_number', 'insurance_number']

        def create(self, validated_data):
            professional = Professional.objects.create_user(
                phone = validated_data['phone'],
                license_number = validated_data.get('license_number'),
                insurance_number = validated_data.get('insurance_number'),
                admin = validated_data.get('admin'),
                address = validated_data.get('address'),
                service = validated_data.get('service'),
            )
            return professional
class ProviderRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id' , 'admin' , 'phone' ,'address']

        def create(self, validated_data):
            provider = Provider.objects.create_user(
                phone = validated_data['phone'],
                admin = validated_data.get('admin'),
                address = validated_data.get('address'),
            )
            return provider