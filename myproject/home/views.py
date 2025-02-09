from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

# Create your views here.


#To render the index.html file
def index(request):
    return render(request, 'home/index.html')

#To render the login.html file
def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s AND passcode=%s", [username, password])
            user=cursor.fetchone()
        
        if user:
            return redirect('thanks')
        
        else:
            return redirect('sorry')

    return render(request, 'home/login.html')


def thanks(request):
    return render(request, 'home/thanks.html')

def sorry(request):
    return render(request, 'home/sorry.html')
