from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout 
from django.contrib.auth.decorators import login_required

"""
Uneccessary import methods

from home.models import UserProfile
from django.contrib.auth.models import User
from django.db import connection

"""

@login_required  # Ensures only logged-in users can access the dashboard

def dashboard(request):
    user = request.user  # Fetch authenticated user

    context = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "department": user.department,
        "gender": user.gender,
    }

    return render(request, "users/dashboard.html", context)


def logout(request):
    django_logout(request)  # Django handles session clearing
    return redirect('home:index')
