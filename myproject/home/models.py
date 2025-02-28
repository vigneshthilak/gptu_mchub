from django.db import models
from django.contrib.auth.models import User
import uuid

# Models for user Profile

class UserProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('dcivil', 'DCIVIL'),
        ('dmech', 'DMECH'),
        ('deee', 'DEEE'),
        ('dece', 'DECE'),
        ('dcse', 'DCSE'),
        ('dmx', 'DMX'),
    ]

    CATEGORY_CHOICES = [
        ('teacher', 'Teacher'),
    ]

    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_id = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # Hashed password (use Django auth)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    user_category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.username

#Model for Authorised user Verification

class AuthUser(models.Model):
    user_id = models.CharField(max_length=20, unique=True)  # Changed from regno to user_id
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.user_id} - {self.email}"


#Models for Password reset token

class PasswordResetToken(models.Model):
    user = models.ForeignKey('home.UserProfile', on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"