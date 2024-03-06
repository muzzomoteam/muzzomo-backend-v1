from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import generics , viewsets
from django.shortcuts import get_object_or_404
from rest_framework import filters
from .models import Job
from user.models import *

from .serializers import JobSerializer , ProfessionalJobSerializer
# Create your views here.

class JobListView(APIView):
  def get(self , request , format = None):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs , many = True)
    return Response(serializer.data)
  def post(self,request , format = None):
    serializer = JobSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data , status= status.HTTP_201_CREATED)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
  
class ActiveJobListView(generics.ListAPIView):
    serializer_class = ProfessionalJobSerializer
    def get_queryset(self):
        return Job.objects.filter(is_completed=False , is_active = True)

class JobDetailView(generics.RetrieveAPIView):
  queryset = Job.objects.all()
  serializer_class = JobSerializer
  def retrieve(self, request , *args , **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return Response(serializer.data)

class ProfessionalJobListView(generics.ListAPIView):
  serializer_class = ProfessionalJobSerializer
  def get_queryset(self):
    user_id = self.kwargs['user_id']
    return Job.objects.filter(professional__id = user_id , is_completed = False, is_active = False)
class ProfessionalJobCompletedobListView(generics.ListAPIView):
  serializer_class = ProfessionalJobSerializer
  def get_queryset(self):
    user_id = self.kwargs['user_id']
    return Job.objects.filter(professional__id = user_id , is_completed = True , is_active = False)
class ProviderJobListView(generics.ListAPIView):
  serializer_class = ProfessionalJobSerializer
  def get_queryset(self):
    user_id = self.kwargs['user_id']
    return Job.objects.filter(provider__id = user_id , is_completed = False,  is_active = False)
class ProviderJobCompletedobListView(generics.ListAPIView):
  serializer_class = ProfessionalJobSerializer
  def get_queryset(self):
    user_id = self.kwargs['user_id']
    return Job.objects.filter(provider__id = user_id , is_completed = True , is_active = False)


class JobUpdateAPIView(APIView):
    def post(self, request, job_id):
        professional_id = request.data.get('professional_id', None)
        if professional_id is None:
            return Response({'message': 'professional_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            job = Job.objects.get(id=job_id)
            job.is_active = False
            # Change professional__id to the provided professional_id
            professionalId = Professional.objects.get(admin = professional_id)
            job.professional = professionalId
            job.save()
            serializer = JobSerializer(job)
            return Response(serializer.data)
        except Job.DoesNotExist:
            return Response({'message': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)