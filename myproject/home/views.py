from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

# Create your views here.

def index(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s AND passcode=%s", [username, password])
            user=cursor.fetchone()
        
        if user:
            return redirect('thankyou')
        
        else:
            return redirect('sorry')

    return render(request, 'home/index.html')

def thank_you(request):
    return render(request, 'home/thankyou.html')

def sorry(request):
    return render(request, 'home/sorry.html')

def signup(request):
    return render(request, 'home/signup.html')