from django.urls import path
from .views import *
urlpatterns = [
  path('jobs-list/' , JobListView.as_view() , name = 'jobs-list'),
  path('active-jobs-list/' , ActiveJobListView.as_view() , name = 'active-jobs-list'),
  path('job-detail/<int:pk>/' , JobDetailView.as_view() , name="job-detail"),
  path('professional-jobs/<int:user_id>/' ,ProfessionalJobListView.as_view() , name="professional-jobs"),
  path('professional-completed-jobs/<int:user_id>/' ,ProfessionalJobCompletedobListView.as_view() , name="professional-completed-jobs"),
  path('provider-jobs/<int:user_id>/' ,ProviderJobListView.as_view() , name="provider-jobs"),
  path('provider-completed-jobs/<int:user_id>/' ,ProviderJobCompletedobListView.as_view() , name="provider-completed-jobs"),
  path('request-job/<int:job_id>/' ,JobUpdateAPIView.as_view(), name="request-job"),
]