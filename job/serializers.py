from rest_framework import serializers
from service.serializers import ServiceSerializer
from user.serializers import ProfessionalSerializer , SimpleUserSerializer , AddressSerializer
from .models import Job

class JobSerializer(serializers.ModelSerializer):
  service_photo = serializers.CharField(source = 'service.photo' , read_only = True)
  service_title = serializers.CharField(source = 'service.title' , read_only = True)
  professional_image = serializers.CharField(source = 'professional.profile_image' , read_only = True)
  professional_first_name = serializers.CharField(source = 'professional.admin.first_name' , read_only = True)
  professional_last_name = serializers.CharField(source = 'professional.admin.last_name' , read_only = True)

  class Meta:
        model = Job
        fields = ['id', 'submit_date', 'start_date','start_time', 'complete_date','complete_time', 'flexable', 'is_active', 'is_completed',
                  'address', 'unit','professional', 'provider', 'service', 'service_image','job_description','service_photo', 'service_title', 
                  'professional_first_name' , 'professional_last_name' ,'professional_image' ]

class ProfessionalJobSerializer(serializers.ModelSerializer):
  service = ServiceSerializer
  simple_user = SimpleUserSerializer
  professional = ProfessionalSerializer
  address = AddressSerializer

  service_photo = serializers.CharField(source = 'service.photo' , read_only = True)
  service_title = serializers.CharField(source = 'service.title' , read_only = True)

  class Meta:
    model = Job
    fields = ['id' , 'submit_date' , 'start_date','start_time', 'complete_date','complete_time', 
              'flexable' , 'is_active' ,'service' , 'professional' , 
              'provider' , 'address', 'unit','service_photo' , 'service_title']

