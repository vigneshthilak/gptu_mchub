from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from .models import UserProfile
from django.core.mail import send_mail
from home.models import UserProfile, PasswordResetToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now, timedelta
from home.models import PasswordResetToken
from django.core.mail import EmailMessage
import uuid
import string
import environ

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
            query = "SELECT * FROM home_userprofile WHERE user_id = %s"
        else:
            query = "SELECT * FROM home_userprofile WHERE username = %s"

        with connection.cursor() as cursor:
            cursor.execute(query, [user_input])
            user = cursor.fetchone()

        if user:
            # User found, check if password matches
            stored_password = user[6]  # Assuming password is stored in index 6
            if check_password(password, stored_password):  # Use check_password to verify hashed password
                return redirect('thanks')
            else:
                messages.error(request, 'Invalid password.')
        else:
            messages.error(request, 'Invalid username/user ID.')

        return redirect('login')

    return render(request, 'home/login.html')

def thanks(request):
    return HttpResponse('<h1>Hello, World!</h1>')

#To render the forgot_password.html file

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email').strip()

        try:
            user = UserProfile.objects.get(email=email)
            token = str(uuid.uuid4())  # Generate unique token
            
            # Save reset token in database
            PasswordResetToken.objects.create(user=user, token=token)

            # Send email with reset link
            reset_link = f"http://192.168.241.240:8000/reset-password/{token}/"
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                "GPTU MC HUB <your-email@example.com>",
                [email],
                fail_silently=False,
            )

            messages.success(request, "Password reset link sent to your email.")
            return redirect('forgot_password')
        except UserProfile.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('forgot_password')

    return render(request, 'home/forgot_password.html')

#To render the reset_password.html file

def reset_password(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        # Check if token is expired (valid for 15 minutes)
        if now() - reset_token.created_at > timedelta(minutes=15):
            messages.error(request, "Password reset link expired.")
            return redirect('forgot_password')

        if request.method == "POST":
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'home/reset_password.html', {"token": token})

            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters.")
                return render(request, 'home/reset_password.html', {"token": token})
            
            special_chars = set(string.punctuation)
            if not any(char in special_chars for char in new_password):
                messages.error(request, 'Password must contain at least one special character!')
                return render(request, 'home/reset_password.html', {"token": token})

            # Update user password
            user = reset_token.user
            user.password = make_password(new_password)
            user.save()

            # Delete token after successful reset
            reset_token.delete()

            messages.success(request, "Password reset successfully. You can now log in.")
            return redirect('login')

    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid or expired reset link.")
        return redirect('forgot_password')

    return render(request, 'home/reset_password.html', {"token": token})


#To render the signup.html file

def signup(request):
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
            messages.error(request, 'Password do not match!')
            return render(request, 'home/signup.html', {
                'first_name': first_name,
                'last_name': last_name, 
                'email': email,
                'user_id': user_id,
                'username': username,
                'department': department,
                'user_category': user_category,
            })
        
        if len(password) < 8:
            messages.error(request, 'Password length must be at least 8 characters!')
            return render(request, 'home/signup.html', {
                'first_name': first_name,
                'last_name': last_name, 
                'email': email,
                'user_id': user_id,
                'username': username,
                'department': department,
                'user_category': user_category,
            })
        
        special_chars = set(string.punctuation)
        if not any(char in special_chars for char in password):
            messages.error(request, 'Password must contain at least one special character!')
            return render(request, 'home/signup.html', {
                'first_name': first_name,
                'last_name': last_name, 
                'email': email,
                'user_id': user_id,
                'username': username,
                'department': department,
                'user_category': user_category,
            })
        
        # Hash the password before saving it
        hashed_password = make_password(password)

        # Save user to the database
        UserProfile.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_id=user_id,
            username=username,
            password=hashed_password,  # Hash password
            department=department,
            user_category=user_category
        )

        return redirect('login')  # Redirect after successful signup

    return render(request, 'home/signup.html')


def contactus(request):
    if request.method == "POST":
        # Get user input and strip spaces
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "No Subject").strip()
        message = request.POST.get("message", "").strip()

        # Set default values if name and email are empty
        if not name:
            name = "Anonymous"
        if not email:
            email = "anonymous@example.com"  # Set a default anonymous email

        # Email content
        email_body = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """

        # Sending Email
        email_send = EmailMessage(
            subject=f"Feedback from {name}",  # Email subject
            body=email_body,  # Email body
            from_email=f'GPTU MC HUB <{email}>',  # Use user's email if provided, else anonymous
            to=['vigneshthilagaraj00@gmail.com'],  # Target email address
        )

        return redirect("contactus")  # Redirect after sending email
    return render(request, 'home/contactus.html')