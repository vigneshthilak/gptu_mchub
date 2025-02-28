from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("forgot-password/", views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path("contact-us/", views.contactus, name='contactus'),
    path("about-us/", views.aboutus, name='aboutus'),
    path("verify-otp/", views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
]