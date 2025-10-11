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
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    differently_abled = models.CharField(max_length=5)
    religion = models.CharField(max_length=10, choices=RELIGION_CHOICES, blank=True, null=True)
    community = models.CharField(max_length=5, choices=COMMUNITY_CHOICES, blank=True, null=True)
    reg_no = models.CharField(max_length=20, unique=True, blank=True, null=True)
    program_name = models.CharField(max_length=10, choices=PROGRAM_NAME_CHOICES)
    program_type = models.CharField(max_length=10, choices=PROGRAM_TYPE_CHOICES)
    year_of_joining = models.DateField(blank=True, null=True)
    mentor_name = models.CharField(max_length=100)
    sslc_mark = models.IntegerField()
    hsc_iti_mark = models.IntegerField(blank=True, null=True)
    govt_school = models.CharField(max_length=5)
    emis_number = models.CharField(max_length=20, blank=True, null=True)
    hosteller = models.CharField(max_length=5)
    extra_curricular = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_father = models.CharField(max_length=10, blank=True, null=True)
    mobile_mother = models.CharField(max_length=10, blank=True, null=True)
    mobile_sibling = models.CharField(max_length=10, blank=True, null=True)
    mobile_guardian = models.CharField(max_length=10, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    single_parent = models.CharField(max_length=5)
    first_graduate = models.CharField(max_length=5)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} ({self.reg_no})"
    

class SSLCMark(models.Model):
    student_name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=20, unique=True)
    dob = models.DateField()

    tamil = models.IntegerField()
    english = models.IntegerField()
    maths = models.IntegerField()
    science = models.IntegerField()
    social = models.IntegerField()

    total = models.IntegerField()
    percentage = models.FloatField()
    
    result = models.CharField(
        max_length=10,
        choices=[('Pass', 'Pass'), ('Fail', 'Fail')],
        default='Pass'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.reg_no}"
    
class HSCMark(models.Model):
    student_name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=20, unique=True)
    dob = models.DateField()

    subject_1 = models.IntegerField()
    subject_2 = models.IntegerField()
    subject_3 = models.IntegerField()
    subject_4 = models.IntegerField()
    subject_5 = models.IntegerField()
    subject_6 = models.IntegerField()

    total = models.IntegerField()
    percentage = models.FloatField()
    result = models.CharField(max_length=10)  # Eg: 'Pass', 'Fail'

    def __str__(self):
        return f"{self.student_name} - {self.reg_no}"
    
class ITIMark(models.Model):
    student_name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=20, unique=True)
    dob = models.DateField()

    subject_1 = models.IntegerField()
    subject_2 = models.IntegerField()
    subject_3 = models.IntegerField()
    subject_4 = models.IntegerField()
    subject_5 = models.IntegerField()
    subject_6 = models.IntegerField()

    total = models.IntegerField()
    percentage = models.FloatField()
    result = models.CharField(max_length=10)  # Eg: 'Pass', 'Fail'

    def __str__(self):
        return f"{self.student_name} - {self.reg_no}"
    
class CollegeMark(models.Model):
    SEMESTER_CHOICES = [(f"{i}", f"{i} Semester") for i in range(1, 7)]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)

    subject1 = models.IntegerField()
    subject2 = models.IntegerField()
    subject3 = models.IntegerField()
    subject4 = models.IntegerField()
    subject5 = models.IntegerField()
    subject6 = models.IntegerField()
    subject7 = models.IntegerField()

    result = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.name} - Sem {self.semester}"