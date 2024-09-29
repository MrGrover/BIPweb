from django.urls import path
from otp_app.views import (RegisterView, LoginView, GenerateOTP, VerifyOTP,
                           DisableOTP, LogoutView, LogoutView)

urlpatterns = [
    path('register', RegisterView.as_view(), name='registration_page'),
    path('login', LoginView.as_view(), name='login_page'),
    path('logout', LogoutView.as_view(), name='logout_page'),
    path('otp/generate', GenerateOTP.as_view(), name='otp_gnrt_page'),
    path('otp/verify', VerifyOTP.as_view(), name='otp_vrf_page'),
    path('otp/disable', DisableOTP.as_view(), name='otp_dsbl_page'),
]