from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.

#To render the index.html file
def index(request):
    return render(request, 'home/index.html')

#To render the login.html file
def login(request):
    if request.method == 'POST':
        user_input = request.POST.get('username')  # Input can be user_id or username
        password = request.POST.get('password')

        # Server-side validation
        if not user_input or not password:
            messages.error(request, 'Both username/user ID and password are required.')
            return redirect('login')

        # Check if the input is numeric (user_id) or alphanumeric (username)
        if user_input.isdigit():
            query = "SELECT * FROM users WHERE user_id = %s AND passcode = %s"
        else:
            query = "SELECT * FROM users WHERE username = %s AND passcode = %s"

        with connection.cursor() as cursor:
            cursor.execute(query, [user_input, password])
            user = cursor.fetchone()

        if user:
            return redirect('thanks')
        else:
            messages.error(request, 'Invalid username/user ID or password.')
            return redirect('login')

    return render(request, 'home/login.html')

def thanks(request):
    return render(request, 'home/thanks.html')

def signup(request):
    return render(request, 'home/signup.html')
