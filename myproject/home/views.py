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
import logging

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

logger = logging.getLogger(__name__)

# To render the Log-In page file
@never_cache
def login(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')  # Input can be user_id or username
        password = request.POST.get('password')

        logger.info(f"Login attempt: user_input={user_input}, password={password}")

        # Server-side validation
        if not user_input or not password:
            messages.error(request, 'Both username/user ID and password are required.')
            return redirect('home:login')

        user_by_username = authenticate(request, username=user_input, password=password)
        user_by_userid = authenticate(request, user_id=user_input, password=password)

        user = user_by_username or user_by_userid
        
        # Try authenticating with user_id or username
        #user = authenticate(request, username=user_input, password=password)
        
        if user:
            auth_login(request, user)  # Django manages session automatically
            logger.info(f"Login successful: user={user}")

            return redirect('users:dashboard')
        else:
            messages.error(request, 'Invalid username/user ID or password.')
            logger.warning(f"Login failed: user_input={user_input}")

        return redirect('home:login')

    response = render(request, 'home/login.html')
    add_never_cache_headers(response)  # Prevents browser from storing login page
    return response

# To render the Account Request page
def acc_req(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_id = request.POST.get('user_id')

        if user_email and user_id:
            try:
                subject = "New Account Request - GPTU MC HUB"
                from_email = f"GPTU MC HUB <{settings.EMAIL_HOST_USER}>"
                to_email = "vigneshthilagaraj00@gmail.com"  # admin's email

                # Plain text content
                text_content = (
                    f"A new user has requested an account.\n\n"
                    f"Email: {user_email}\n"
                    f"User ID: {user_id}\n\n"
                    f"Please review and take appropriate action.\n\n"
                    f"Regards,\nGPTU MC HUB"
                )

                # HTML content
                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
                    <h2 style="color: #2c3e50;">New Account Request</h2>
                    <p>You have received a new account request from a user.</p>
                    <p><strong>Email Address:</strong> {user_email}</p>
                    <p><strong>User ID:</strong> {user_id}</p>
                    <p>Please review and take the necessary action to approve or deny this request.</p>
                    <br>
                    <p>Regards,</p>
                    <p style="font-weight: bold; color: #2c3e50;">GPTU MC HUB System</p>
                    <hr>
                    <small>This is an automated message. Please do not reply directly to this email.</small>
                </body>
                </html>
                """

                msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, "Your request has been sent successfully!")
            except Exception as e:
                messages.error(request, f"Failed to send email. Error: {e}")
        else:
            messages.error(request, "Please provide both Email and User ID.")

        return redirect('home:acc_req')

    return render(request, 'home/acc_req.html')


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