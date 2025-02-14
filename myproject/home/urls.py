from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login, name='login'),
    path("thanks/", views.thanks, name='thanks'),
    path('signup/', views.signup_view, name='signup'),
]