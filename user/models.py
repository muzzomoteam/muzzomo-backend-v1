
# -----------------------------
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,Group,Permission
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from service.models import *


# >>>...................>>...............>>
# USERMODELS
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Province(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Address(models.Model):
    street = models.CharField(max_length=255, null = True)
    unit = models.CharField(max_length = 255 , null = True)
    city  = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.street)
# >>>>---------------------------<<-----

# USER MODELS

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length = 255, unique = True, verbose_name = _("Email Address"))
    first_name = models.CharField(max_length = 100, verbose_name = _('First Name'))
    last_name = models.CharField(max_length = 100, verbose_name=_('Last Name'))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default = False)
    is_verified = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_professional = models.BooleanField(default = False)
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now = True)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        }
        
class OneTimePassword(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    code = models.CharField(max_length = 6, unique = True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"
    
    
# employee
class Professional(models.Model):
    admin = models.OneToOneField(User , on_delete=models.CASCADE)
    license_number = models.CharField(max_length = 100)
    insurance_number = models.CharField(max_length = 100)
    service  = models.ForeignKey(Service, on_delete = models.CASCADE)
    profile_image = models.ImageField(upload_to='proprofile/' , blank= True, null=True)
    phone = PhoneNumberField(blank = True, null = True)
 
    address = models.ForeignKey(Address, on_delete = models.CASCADE)
    def __str__ (self):
        return str(self.admin)
    
class Provider(models.Model):
    profile_image = models.ImageField(upload_to='userprofile/' , blank= True, null=True)
    phone = PhoneNumberField()
    address = models.ForeignKey(Address, on_delete = models.CASCADE , blank= True, null=True)
    admin = models.OneToOneField(User, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.admin)
    