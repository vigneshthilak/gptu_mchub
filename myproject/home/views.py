from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, AuthUser, PasswordResetToken
from django.core.mail import send_mail
from home.models import UserProfile, PasswordResetToken
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now, timedelta
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.cache import never_cache
from django.utils.cache import add_never_cache_headers
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

"""

# Create your views here.

#To render the index.html file
def index(request):
    return render(request, 'home/index.html')

#To render the login.html file
@never_cache 
def login(request):
    if request.method == 'POST':
        user_input = request.POST.get('username')  # Input can be user_id or username
        password = request.POST.get('password')

        # Server-side validation
        if not user_input or not password:
            messages.error(request, 'Both username/user ID and password are required.')
            return redirect('home:login')
        
        # Try authenticating with user_id or username
        user = authenticate(request, user_id=user_input, password=password) or \
               authenticate(request, username=user_input, password=password)
        
        if user:
            auth_login(request, user)  # Django manages session automatically
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Invalid username/user ID or password.')

        return redirect('home:login')

    response = render(request, 'home/login.html')
    add_never_cache_headers(response)  # Prevents browser from storing login page
    return response

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
            reset_link = f"http://{settings.LOCAL_IP}:8000/reset-password/{token}/"
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                "GPTU MC HUB <your-email@example.com>",
                [email],
                fail_silently=False,
            )

            messages.success(request, "Password reset link sent to your email.")
            return redirect('home:forgot_password')
        except UserProfile.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('home:forgot_password')

    return render(request, 'home/forgot_password.html')


#To render the reset_password.html file

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

def send_otp(email, request):
    otp = ''.join(random.choices(string.digits, k=6))  # Generate 6-digit OTP
    expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    request.session['otp'] = otp
    request.session['otp_expiry'] = expiry_time.timestamp()

    subject = "Your OTP for Account Verification"
    message = f"Your OTP is: {otp}. It will expire in 1 minute. Do not share this with anyone."

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])  # Send email
    return otp


#To render the signup.html file

def signup(request):
    if request.method == "POST":

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
                'gender': gender,
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
                'gender': gender,
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
        
        # Validate user_id and email against auth_users
        if not AuthUser.objects.filter(user_id=user_id, email=email).exists():
            messages.error(request, "You're not eligible to create an account!")
            return render(request, 'home/signup.html')

        # Hash the password before saving it
        #hashed_password = make_password(password)

        # Send OTP for verification
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

#To verify the otp

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


#To resend the OTP

def resend_otp(request):
    if request.method == "POST":
        user_data = request.session.get("user_data", {})
        user_email = user_data.get("email")

        if not user_email:
            messages.error(request, "User email not found. Please sign up again.")
            return redirect("home:verify_otp")

        # Debugging: Print Old OTP Before Replacing
        old_otp = request.session.get("otp")
        print(f"Old OTP before update: {old_otp}")

        # Remove Old OTP from Session
        request.session.pop("otp", None)
        request.session.pop("otp_expiry", None)

        # Generate a New OTP
        new_otp = ''.join(random.choices(string.digits, k=6))
        expiry_time = now() + datetime.timedelta(minutes=1)

        # Store the New OTP in Session
        request.session["otp"] = new_otp
        request.session["otp_expiry"] = expiry_time.timestamp()
        request.session.modified = True  # Ensures Django saves session changes
        request.session.save() #Ensure session is saved immediately.

        # Debugging: Print New OTP After Replacing
        print(f"New OTP after update: {request.session.get('otp')}, Expiry: {request.session.get('otp_expiry')}")

        # Send OTP via Email
        subject = "Your New OTP for Account Verification"
        message = f"Your new OTP is: {new_otp}. It will expire in 1 minute. Do not share this with anyone."

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
            messages.success(request, "A new OTP has been sent to your email.")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

        return redirect("home:verify_otp")

    return redirect("home:verify_otp")

#To render the contactus.html file

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
            from_email="yourverifiedemail@example.com",  # Use a valid email
            to=['vigneshthilagaraj00@gmail.com'],
            reply_to=[email]  # This allows replies to go to the user's email
        )

        try:
            email_send.send()
            return redirect("home:contactus")  # Redirect after sending email
        except Exception as e:
            print("Email sending failed:", e)  # Debugging info

    return render(request, 'home/contactus.html')

def aboutus(request):
    return render(request, 'home/aboutus.html')