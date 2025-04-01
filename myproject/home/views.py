from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, PasswordResetToken
from home.models import UserProfile, PasswordResetToken
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now, timedelta
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.cache import never_cache
from django.utils.cache import add_never_cache_headers
from django.core.mail import EmailMultiAlternatives
import uuid
import string
import random
import datetime

"""
Uneccessary import methods

from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail

"""

# Create your views here.

# To render the Home page of the web application (index.html)
def index(request):
    return render(request, 'home/index.html')

# To render the Log-In page file
@never_cache
def login(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')  # Input can be user_id or username
        password = request.POST.get('password')

        # Server-side validation
        if not user_input or not password:
            messages.error(request, 'Both username/user ID and password are required.')
            return redirect('home:login')
        
        # Try authenticating with user_id or username
        user = authenticate(request, username=user_input, password=password)
        
        if user:
            auth_login(request, user)  # Django manages session automatically
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Invalid username/user ID or password.')

        return redirect('home:login')

    response = render(request, 'home/login.html')
    add_never_cache_headers(response)  # Prevents browser from storing login page
    return response

# To render the Forgot Password page
# Used to change the users password if the user forgot their password
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email').strip()

        try:
            user = UserProfile.objects.get(email=email)
            token = str(uuid.uuid4())  # Generate unique token
            
            # Save reset token in database
            PasswordResetToken.objects.create(user=user, token=token)

            # Create reset link
            reset_link = f"http://{settings.LOCAL_IP}:8000/reset-password/{token}/"

            subject = "GPTU MC HUB - Password Reset Request"
            from_email = f"GPTU MC HUB <{settings.EMAIL_HOST_USER}>"
            text_content = f"Hello {user.first_name},\n\nWe received a request to reset your password.\nClick the following link to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email.\n\nRegards,\nGPTU MC HUB Team"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
                <h2>GPTU MC HUB - Password Reset Request</h2>
                <p>Hello <strong>{user.first_name}</strong>,</p>
                <p>We received a request to reset your password. Please click the button below to reset it:</p>
                <p style="margin: 30px 0;">
                    <a href="{reset_link}" target="_blank" 
                       style="background-color: #2c3e50; color: #fff; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block;">
                       Reset Password
                    </a>
                </p>
                <p>If the button above does not work, you can also copy and paste this link in your browser:</p>
                <p><a href="{reset_link}" target="_blank">{reset_link}</a></p>
                <br>
                <p>If you did not request a password reset, please ignore this email or contact support.</p>
                <br>
                <p>Regards,</p>
                <p style="font-weight: bold; color: #2c3e50;">GPTU MC HUB Team</p>
                <hr>
                <small>This is an automated email; please do not reply.</small>
            </body>
            </html>
            """

            # Send HTML email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Password reset link sent to your email.")
            return redirect('home:forgot_password')
        except UserProfile.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('home:forgot_password')

    return render(request, 'home/forgot_password.html')


# To render the Reset Password page according to the reset link which is sent to user's corresponding E-Mail ID
def reset_password(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        # Check if token is expired (valid for 15 minutes)
        if now() - reset_token.created_at > timedelta(minutes=15):
            messages.error(request, "Password reset link expired.")
            return redirect('home:forgot_password')

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

            messages.success(request, "Password reset successfully.")
            return redirect('home:login')

    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid or expired reset link.")
        return redirect('home:forgot_password')

    return render(request, 'home/reset_password.html', {"token": token})

# Function used to Generate and send the 6 digit OTP to users corresponding E-Mail ID
def send_otp(email, request):
    otp = ''.join(random.choices(string.digits, k=6))  # Generate 6-digit OTP
    expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    request.session['otp'] = otp
    request.session['otp_expiry'] = expiry_time.timestamp()

    subject = "Your GPTU MC HUB Email Verification Code"
    from_email = f"GPTU MC HUB <{settings.EMAIL_HOST_USER}>"
    text_content = f"Hello,\n\nYour OTP for email verification is: {otp}\nThis OTP will expire in 1 minute.\n\nPlease do not share this code with anyone.\n\nRegards,\nGPTU MC HUB Team"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>GPTU MC HUB - Email Verification</h2>
        <p>Hello,</p>
        <p>Your One-Time Password (OTP) for verification is:</p>
        <h1 style="color: #2c3e50;">{otp}</h1>
        <p>This OTP will expire in <strong>1 minute</strong>.</p>
        <p>Please do not share this code with anyone.</p>
        <br>
        <p>Regards,</p>
        <p style="color: #2c3e50; font-weight: bold;">GPTU MC HUB Team</p>
        <hr>
        <small>This is an automated email; please do not reply.</small>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return otp


# To render the Signup page
def signup(request):
    if request.method == "POST":

        # To get the input values from the users to create an account
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        user_id = request.POST.get('userId', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirmPassword', '').strip()
        department = request.POST.get('department', '').strip()
        gender = request.POST.get('gender', '').strip()

        # Check if any field is empty
        if not all([first_name, last_name, email, user_id, username, password, confirm_password, department, gender]):
            messages.error(request, 'All fields are required! Please fill in all fields.')
            return render(request, 'home/signup.html')
        
        # To Ensure the given username is starts with '@'
        if username[0] != '@':
            messages.error(request, "The Username must start with '@'")
            return render(request, 'home/signup.html', {
                'first_name': first_name,
                'last_name': last_name, 
                'email': email,
                'user_id': user_id,
                'department': department,
                'gender': gender,
            })
        
        # To Ensure the given username contains only lowercase letters
        if not username.islower():
            messages.error(request, 'Username must contain only lowercase letters.')
            return render(request, 'home/signup.html', {
                'first_name': first_name,
                'last_name': last_name, 
                'email': email,
                'user_id': user_id,
                'department': department,
                'gender': gender,
            })


        # To check the Password and Confirm Password both are same or not
        if password != confirm_password:
            messages.error(request, 'Password do not match!')
            return render(request, 'home/signup.html', {
                'first_name': first_name,
                'last_name': last_name, 
                'email': email,
                'user_id': user_id,
                'username': username,
                'department': department,
                'gender': gender,
            })
        
        # To Ensure the given password has at least 8 charactes
        if len(password) < 8:
            messages.error(request, 'Password length must be at least 8 characters!')
            return render(request, 'home/signup.html', {
                'first_name': first_name,
                'last_name': last_name, 
                'email': email,
                'user_id': user_id,
                'username': username,
                'department': department,
                'gender': gender,
            })
        
        # To Ensure the given password contains at least one special character
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
                'gender': gender,
            })

        # Check if username already exists
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another one.")
            return render(request, 'home/signup.html', {
                'first_name': first_name,
                'last_name': last_name, 
                'email': email,
                'user_id': user_id,
                'department': department,
                'gender': gender,
            })
        
        # Check if user_id already exists
        if UserProfile.objects.filter(user_id=user_id).exists():
            messages.error(request, "User ID already exists.")
            return render(request, 'home/signup.html', {
                'first_name': first_name,
                'last_name': last_name, 
                'email': email,
                'username': username,
                'department': department,
                'gender': gender,
            })
        
        """
        # Validate user_id and email against auth_users
        if not AuthUser.objects.filter(user_id=user_id, email=email).exists():
            messages.error(request, "You're not eligible to create an account!")
            return render(request, 'home/signup.html')
        """

        # Calling the send_otp() to send the otp if the given inputs are correct
        otp = send_otp(email, request)  
        request.session['otp'] = otp  
        request.session['user_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'user_id': user_id,
            'username': username,
            'department': department,
            'gender': gender,
            'password': password,  # Store plain password temporarily for user creation
        }

        return redirect('home:verify_otp')  # Redirect to OTP verification page

    return render(request, 'home/signup.html')

# To verify the otp
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp", "").strip()
        stored_otp = request.session.get("otp")
        otp_expiry = request.session.get("otp_expiry")

        # Validate OTP existence and expiration
        if not stored_otp or not otp_expiry or now().timestamp() > otp_expiry:
            messages.error(request, "OTP has expired! Please request a new one.")
            return redirect("home:verify_otp")

        # Validate OTP match
        if entered_otp == stored_otp:
            user_data = request.session.get("user_data", {})

            if user_data:
                try:
                    # Create user in Django authentication system
                    user = UserProfile.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],  # Django hashes password automatically
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        user_id=user_data['user_id'],  
                        department=user_data['department'],
                        gender=user_data['gender'],
                    )

                    # Clear session data
                    request.session.pop("otp", None)
                    request.session.pop("user_data", None)
                    request.session.pop("otp_expiry", None)

                    messages.success(request, "Account created successfully!")
                    return redirect("home:login")
                
                except Exception as e:
                    messages.error(request, f"Error creating account: {e}")
                    return redirect("home:verify_otp")
        else:
            messages.error(request, "Invalid OTP! Please try again.")
            return render(request, 'home/verify_otp.html')

    return render(request, 'home/verify_otp.html')


# To resend the OTP
def resend_otp(request):
    if request.method == "POST":
        user_data = request.session.get("user_data", {})
        user_email = user_data.get("email")

        if not user_email:
            messages.error(request, "User email not found. Please sign up again.")
            return redirect("home:verify_otp")

        # Remove Old OTP from Session
        request.session.pop("otp", None)
        request.session.pop("otp_expiry", None)

        # Generate new OTP and expiry
        new_otp = ''.join(random.choices(string.digits, k=6))
        expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
        request.session["otp"] = new_otp
        request.session["otp_expiry"] = expiry_time.timestamp()
        request.session.modified = True

        # HTML email content (copied from your send_otp style)
        subject = "Your New OTP for GPTU MC HUB Verification"
        from_email = f"GPTU MC HUB <{settings.EMAIL_HOST_USER}>"
        text_content = f"Hello,\n\nYour new OTP for verification is: {new_otp}\nThis OTP will expire in 1 minute.\n\nPlease do not share this code with anyone.\n\nRegards,\nGPTU MC HUB Team"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2>GPTU MC HUB - Email Verification</h2>
            <p>Hello,</p>
            <p>Your new One-Time Password (OTP) for verification is:</p>
            <h1 style="color: #2c3e50;">{new_otp}</h1>
            <p>This OTP will expire in <strong>1 minute</strong>.</p>
            <p>Please do not share this code with anyone.</p>
            <br>
            <p>Regards,</p>
            <p style="color: #2c3e50; font-weight: bold;">GPTU MC HUB Team</p>
            <hr>
            <small>This is an automated email; please do not reply.</small>
        </body>
        </html>
        """

        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [user_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, "A new OTP has been sent to your email.")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

        return redirect("home:verify_otp")

    return redirect("home:verify_otp")

#To render the Contact Us page
def contactus(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "No Subject").strip()
        message = request.POST.get("message", "").strip()

        if not name:
            name = "Anonymous"
        if not email:
            email = "anonymous@example.com"

        email_body = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """

        email_send = EmailMessage(
            subject=f"Feedback from {name}",
            body=email_body,
            from_email=f"GPTU MC HUB <{settings.EMAIL_HOST_USER}>",  # Use a valid email
            to=['www.mr.comp@gmail.com'],
            reply_to=[email]  # This allows replies to go to the user's email
        )

        try:
            email_send.send()
            return redirect("home:contactus")  # Redirect after sending email
        except Exception as e:
            print("Email sending failed:", e)  # Debugging info

    return render(request, 'home/contactus.html')

# To render the About Us page
def aboutus(request):
    return render(request, 'home/aboutus.html')