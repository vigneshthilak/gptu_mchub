from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from .models import UserProfile, AuthUser, PasswordResetToken
from django.core.mail import send_mail
from home.models import UserProfile, PasswordResetToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now, timedelta
from django.core.mail import EmailMessage
from django.conf import settings
import uuid
import string
import random
import datetime

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
            return redirect('home:login')

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
                request.session['user_id'] = user[4]
                request.session['username'] = user[5]
                request.session['department'] = user[7]
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Invalid password.')
        else:
            messages.error(request, 'Invalid username/user ID.')

        return redirect('home:login')

    return render(request, 'home/login.html')

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
            messages.error(request, 'All fields are required! Please fill in all fields.')
            return render(request, 'home/signup.html')

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

        # Validate user_id and email against auth_users
        if AuthUser.objects.filter(user_id=user_id, email=email).exists():
            otp = send_otp(email, request)  # Send OTP to email
            request.session['otp'] = otp  # Store OTP in session
            request.session['user_data'] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'user_id': user_id,
                'username': username,
                'department': department,
                'user_category': user_category,
                'password': hashed_password,
            }

            return redirect('home:verify_otp')  # Redirect to OTP verification page
        else:
            messages.error(request, "You're not eligible to create an account!")
            return render(request, 'home/signup.html')

    return render(request, 'home/signup.html')

#To verify the otp

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp", "").strip()
        stored_otp = request.session.get("otp")
        otp_expiry = request.session.get("otp_expiry")

        # Debugging logs
        print(f"Entered OTP: {entered_otp}")
        print(f"Stored OTP: {stored_otp}")
        print(f"Current Time: {now().timestamp()}")
        print(f"OTP Expiry: {otp_expiry}")

        # Validate OTP existence and expiration
        if not stored_otp or not otp_expiry or now().timestamp() > otp_expiry:
            messages.error(request, "OTP has expired! Please request a new one.")
            return redirect("home:verify_otp")

        # Validate OTP match
        if entered_otp == stored_otp:
            user_data = request.session.get("user_data", {})

            if user_data:
                try:
                    # Save user data in home_userprofile
                    UserProfile.objects.create(
                        first_name=user_data.get('first_name', ''),
                        last_name=user_data.get('last_name', ''),
                        email=user_data.get('email', ''),
                        user_id=user_data.get('user_id', ''),  # Changed from regno to user_id
                        username=user_data.get('username', ''),
                        department=user_data.get('department', ''),
                        user_category=user_data.get('user_category', ''),
                        password=user_data.get('password', ''),  # Password is hashed in model
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

        # 🔍 Debugging: Print Old OTP Before Replacing
        old_otp = request.session.get("otp")
        print(f"Old OTP before update: {old_otp}")

        # ✅ Remove Old OTP from Session
        request.session.pop("otp", None)
        request.session.pop("otp_expiry", None)

        # ✅ Generate a New OTP
        new_otp = ''.join(random.choices(string.digits, k=6))
        expiry_time = now() + datetime.timedelta(minutes=1)

        # ✅ Store the New OTP in Session
        request.session["otp"] = new_otp
        request.session["otp_expiry"] = expiry_time.timestamp()
        request.session.modified = True  # Ensures Django saves session changes
        request.session.save() #Ensure session is saved immediately.

        # 🔍 Debugging: Print New OTP After Replacing
        print(f"New OTP after update: {request.session.get('otp')}, Expiry: {request.session.get('otp_expiry')}")

        # ✅ Send OTP via Email
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