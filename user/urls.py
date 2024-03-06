from django.contrib import admin
from rest_framework_simplejwt.views import TokenBlacklistView
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name = 'register'),
    path('verify/', VerifyUserEmail.as_view(), name = 'VerifyEmail'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestAuthenticationView.as_view(), name='granted'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    # --------------------------------------------------------------------------------------------------------------------------
    
    path('provider/<int:admin_id>/', ProviderUserRetrieveAPIView.as_view(), name='provider_user_detail'),
    path('professional/<int:admin_id>/', ProfessionalUserRetrieveAPIView.as_view(), name='professional_user_detail'),
    path('get-user-id/<str:email>/', GetUserIdByEmail.as_view(), name='get_user_id_by_email'),
    path('professional-register/', RegisterProfessional.as_view(), name='professional-register'),
    path('provider-register/', ProviderProfessional.as_view(), name='provider-register'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('update-professional-status/<int:user_id>/', UpdateProfessionalStatus.as_view(), name='update-professional-status'),
]