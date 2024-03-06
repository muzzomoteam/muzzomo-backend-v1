from django.db import models
from service.models import *
from user.models import *
# Create your models here.
class Job(models.Model):
    submit_date = models.DateField(auto_now_add = True)
    start_date = models.DateField(null = True)
    start_time = models.TimeField(null = True)
    complete_date = models.DateField(null = True)
    complete_time = models.TimeField(null = True)
    flexable = models.BooleanField(default = False)
    is_active = models.BooleanField(default =True)
    is_completed = models.BooleanField(default = False)
    address = models.CharField(max_length = 255 , null = True)
    unit = models.CharField(max_length = 255 , null = True)
    professional = models.ForeignKey(Professional, on_delete = models.SET_NULL, null = True, blank = True)
    provider = models.ForeignKey(Provider, on_delete = models.CASCADE)
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    service_image = models.ImageField(upload_to='job_image/' , blank=True , null=True)
    job_description = models.CharField(max_length = 500 , null = True)
    def __str__(self):
        return str(self.service)+' by '+str(self.professional)+' for '+ str(self.provider)