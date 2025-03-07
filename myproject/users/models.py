from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Others', 'Others'),
    ]

    PROGRAM_NAME_CHOICES = [
        ('DCIVIL', 'DCIVIL'),
        ('DMECH', 'DMECH'),
        ('DEEE', 'DEEE'),
        ('DECE', 'DECE'),
        ('DCSE', 'DCSE'),
        ('DMX', 'DMX'),
        ('DMT', 'DMT'),
    ]

    PROGRAM_TYPE_CHOICES = [
        ('Regular', 'Regular'),
        ('Lateral', 'Lateral'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    RELIGION_CHOICES = [
        ('Hindu', 'Hindu'),
        ('Christian', 'Christian'),
        ('Islam', 'Islam'),
        ('Other', 'Other'),
    ]

    COMMUNITY_CHOICES = [
        ('BC', 'BC'),
        ('MBC', 'MBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OC', 'OC'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    reg_no = models.CharField(max_length=20, unique=True)
    program_name = models.CharField(max_length=10, choices=PROGRAM_NAME_CHOICES)
    program_type = models.CharField(max_length=10, choices=PROGRAM_TYPE_CHOICES)
    year_of_joining = models.DateField(blank=True, null=True)
    mentor_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    differently_abled = models.CharField(max_length=5, default='No')
    mobile_father = models.CharField(max_length=10, blank=True, null=True)
    mobile_mother = models.CharField(max_length=10, blank=True, null=True)
    mobile_sibling = models.CharField(max_length=10, blank=True, null=True)
    mobile_guardian = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    emis_number = models.CharField(max_length=20, blank=True, null=True)
    sslc_mark = models.DecimalField(max_digits=5, decimal_places=2)
    hsc_iti_mark = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    govt_school = models.CharField(max_length=5, default='No')
    first_graduate = models.CharField(max_length=5, default='No')
    hosteller = models.CharField(max_length=5, default='No')
    single_parent = models.CharField(max_length=5, default='No')
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=15, blank=True, null=True)
    extra_curricular = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    religion = models.CharField(max_length=10, choices=RELIGION_CHOICES, blank=True, null=True)
    community = models.CharField(max_length=5, choices=COMMUNITY_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} ({self.reg_no})"
