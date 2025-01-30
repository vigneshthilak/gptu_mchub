from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("signup/", views.signup, name='signup'),
    path("thankyou/", views.thank_you, name='thankyou'),
    path("sorry/", views.sorry, name='sorry')
]