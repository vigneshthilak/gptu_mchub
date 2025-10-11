from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login, name='login'),
    path("account-request/", views.acc_req, name='acc_req'),
    path("forgot-password/", views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path("contact-us/", views.contactus, name='contactus'),
    path("about-us/", views.aboutus, name='aboutus'),
]