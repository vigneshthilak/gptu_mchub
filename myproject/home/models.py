from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

"""
Uneccessary import methods

from django.contrib.auth.models import User

"""


# Models for user Profile

class UserProfile(AbstractUser):
    DEPARTMENT_CHOICES = [
        ('DCIVIL', 'DCIVIL'),
        ('DMECH', 'DMECH'),
        ('DEEE', 'DEEE'),
        ('DECE', 'DECE'),
        ('DCSE', 'DCSE'),
        ('DMX', 'DMX'),
        ('DMT', 'DMT'),
        ('OTHERS', 'OTHERS'),
    ]

    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('others', 'Others')
    ]

    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_id = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Female')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_id', 'email']

    def __str__(self):
        return self.username

#Model for Authorised user Verification

class AuthUser(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.CharField(max_length=20, unique=True)  # Changed from regno to user_id
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.user_id} - {self.email}"


#Models for Password reset token

class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"
