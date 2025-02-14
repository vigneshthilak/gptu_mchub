from django.db import models

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
