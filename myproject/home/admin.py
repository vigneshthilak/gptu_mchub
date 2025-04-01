from django.contrib import admin
from .models import UserProfile
from .models import PasswordResetToken
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import string
import random

def generate_password():
    """Generate a random 10-character password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(10))

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'department', 'gender')
    search_fields = ('user_id', 'email')
    list_filter = ('department', 'gender')

    # **HIDE the password field in Admin Panel**
    exclude = ('password',)

    def save_model(self, request, obj, form, change):
        if not change:  # If the user is being created (not updated)
            password = generate_password()
            obj.set_password(password)  # Hash and set password
            obj.save()

            # Email subject
            subject = "Your GPTU MC HUB Account Has Been Successfully Created!"
            from_email = f"GPTU MC HUB <{settings.EMAIL_HOST_USER}>"
            text_content = f"Dear User,\nYour account has been successfully created. Below are your login details\nUser ID: {obj.user_id}\nPassword: {password}\nPlease log in and change your password immediately for security reasons.\n\nBest Regards,\nGPTU MC HUB Team."

            # HTML email content
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #333;">Welcome to GPTU MC HUB!</h2>
                <p style="color: #333;">Dear <strong>User</strong>,</p>
                <p>Your account has been successfully created. Below are your login details:</p>
                <p style="color: #333;"><strong>User ID:</strong>&nbsp;&nbsp;&nbsp;&nbsp;{obj.user_id}</p>
                <p style="color: #333;"><strong>Password:</strong>&nbsp;&nbsp;&nbsp;{password}</p>
                <p>Please log in and change your password immediately for security reasons.</p>
                <p>If you have any issues, feel free to contact our support team.</p>
                <br>
                <p>Regards,</p>
                <p style="font-weight: bold; color: #333;">GPTU MC HUB Team</p>
                <hr>
                <small>This is an automated email; please do not reply.</small>
            </body>
            </html>
            """

            # Send HTML email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [obj.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        super().save_model(request, obj, form, change)
