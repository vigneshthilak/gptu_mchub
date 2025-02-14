from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from .models import UserProfile

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
            query = "SELECT * FROM home_userprofile WHERE user_id = %s AND password = %s"
        else:
            query = "SELECT * FROM home_userprofile WHERE username = %s AND password = %s"

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


#To render the signup.html file

def signup_view(request):
    if request.method == "POST":
        # Print all form data for debugging
        print("Received POST Data:", request.POST)

        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        user_id = request.POST.get('userId', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirmPassword', '').strip()
        department = request.POST.get('department', '').strip()
        user_category = request.POST.get('userCategory', '').strip()

        # Debugging: Print each value
        print(f"first_name: {first_name}, last_name: {last_name}, email: {email}, user_id: {user_id}")
        print(f"username: {username}, password: {password}, confirm_password: {confirm_password}")
        print(f"department: {department}, user_category: {user_category}")

        # Check if any field is empty
        if not all([first_name, last_name, email, user_id, username, password, confirm_password, department, user_category]):
            return HttpResponse("All fields are required! Please fill in all fields.", status=400)

        # Check if passwords match
        if password != confirm_password:
            return HttpResponse("Passwords do not match!", status=400)

        # Save user to the database
        UserProfile.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_id=user_id,
            username=username,
            password=password,  # Hash password
            department=department,
            user_category=user_category
        )

        return redirect('login')  # Redirect after successful signup

    return render(request, 'home/signup.html')
