from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as django_logout 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Student
from home.models import UserProfile
from django.contrib.auth.models import AnonymousUser
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.hashers import check_password, make_password
from django.db.models.functions import Concat, Lower
from django.db.models import Value
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import pandas as pd
import pdfkit
import os
import io
import base64
import string
import datetime
import random
import smtplib

"""
Uneccessary import methods

from home.models import UserProfile
from django.contrib.auth.models import User
from django.db import connection
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


"""
# To render the Dashboard for the corresponding logged-in users
# Only logged-in users can access the dashboard
@login_required(login_url='/')  # Ensures only logged-in users can access the dashboard
@cache_control(no_store=True, no_cache=True, must_revalidate=True)  # Prevents browser from storing dashboard page
def dashboard(request):
    user = request.user  # Fetch authenticated user

    # Check for missing profile fields
    missing_fields = []

    if not user.first_name:
        missing_fields.append("First Name")
    if not user.last_name:
        missing_fields.append("Last Name")
    if not user.email:
        missing_fields.append("Email")
    if not user.user_id:
        missing_fields.append("User ID")
    if not user.department:
        missing_fields.append("Department")

    # Store in session only if missing fields exist
    if missing_fields:
        request.session['missing_fields'] = missing_fields
    else:
        request.session.pop('missing_fields', None)

    context = {
        "mentor_first_name": user.first_name,
        "mentor_last_name": user.last_name,
        "mentor_department": user.department,
        "mentor_gender": user.gender,
    }

    return render(request, "users/dashboard.html", context)

# To render the Add Student page
# Only logged-in users can access this page
def add_stu(request):
    user = request.user

    # Redirect to home:index if the user is not authenticated
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return redirect('home:index')

    context = {
        "mentor_name": user.first_name,
    }

    # Get the input of the student details from the user
    if request.method == 'POST':
        #Personal Details
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        dob = parse_date(request.POST.get("dob"))
        gender = request.POST.get("gender")
        blood_group = request.POST.get("blood_group")
        mother_tongue = request.POST.get("mother_tongue")
        differently_abled = request.POST.get("differently_abled")
        religion = request.POST.get("religion")
        community = request.POST.get("community")

        #Educational Details
        reg_no = request.POST.get("reg_no")
        program_name = request.POST.get("program_name")
        program_type = request.POST.get("program_type")
        year_of_joining = parse_date(request.POST.get("year_of_joining"))
        mentor_name = request.POST.get("mentor_name")
        sslc_mark = request.POST.get("sslc_mark")
        hsc_iti_mark = request.POST.get("hsc_iti_mark")
        govt_school = request.POST.get("govt_school")
        emis_number = request.POST.get("emis_number")
        hosteller = request.POST.get("hosteller")
        extra_curricular = request.POST.get("extra_curricular")
        achievements = request.POST.get("achievements")

        #Identification Details 
        aadhar_number = request.POST.get("aadhar_number")

        #Family Details
        father_name = request.POST.get("father_name")
        mother_name = request.POST.get("mother_name")
        mobile_father = request.POST.get("mobile_father")
        mobile_mother = request.POST.get("mobile_mother")
        mobile_sibling = request.POST.get("mobile_sibling")
        mobile_guardian = request.POST.get("mobile_guardian")
        father_occupation = request.POST.get("father_occupation")
        single_parent = request.POST.get("single_parent")
        first_graduate = request.POST.get("first_graduate")

        #Contact Details
        email = request.POST.get("email")
        address = request.POST.get("address")
        district = request.POST.get("district")
        pin_code = request.POST.get("pin_code")

        #Bank Details
        bank_name = request.POST.get("bank_name")
        branch_name = request.POST.get("branch_name")
        account_number = request.POST.get("account_number")
        ifsc_code = request.POST.get("ifsc_code")

        # Display the error message if the Firstname error occurs
        first_name_error = {}

        if not first_name:
            first_name_error['first_name_error'] = True

        if first_name_error:
            messages.error(request, "Please Enter the Name of the student.")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **first_name_error,  # Pass error flags to template
            })
        
        # Display the error message if the Lastname error occurs
        last_name_error = {}
        
        if not last_name:
            last_name_error['last_name_error'] = True

        if last_name_error:
            messages.error(request, "Please Enter the Lastname of the Student.")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **last_name_error,  # Pass error flags to template
            })

        # Display the error message if the Reg.No error occurs
        reg_no_error = {}

        if Student.objects.filter(reg_no=reg_no).exists():
            reg_no_error["reg_no_error"] = True

        if reg_no_error:
            messages.error(request, "The Register Number is already exists.")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **reg_no_error,  # Pass error flags to template
            })
        
        # Display the error message if the Program name or Program type error occurs
        program_errors = {}

        if not program_name:
            program_errors["program_name_error"] = True

        if not program_type:
            program_errors["program_type_error"] = True

        # If errors exist, re-render the form with error flags
        if program_errors:
            messages.error(request, "Please select the Program Name & Program Type.")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **program_errors,  # Pass error flags to template
            })
        
        # Display the error message if the Gender error occurs
        gender_error = {}

        if not gender:
            gender_error["gender_error"] = True
        
        if gender_error:
            messages.error(request, "Pleases select the Gender.")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **gender_error  # Pass error indicators
            })

        # It will set the value as No if the user does not give the value
        if not differently_abled:
            differently_abled = 'No'

        # Display the error message if the Email error occurs
        email_error = {}

        if Student.objects.filter(email=email).exists():
            email_error["email_error"] = True

        if email_error:
            messages.error(request, "The E-Mail ID is already exists")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **email_error  # Pass error indicators
            })
        
        # If the user does not give the Aadhar Number then it will display the error message
        aadhar_not_error = {}
        
        if not aadhar_number:
            aadhar_not_error["aadhar_not_error"] = True

        if aadhar_not_error:
            messages.error(request, "Please Enter the Aadhar Card Number.")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **aadhar_not_error  # Pass error indicators
            })

        # Display the error message if the Aadhar Number error occurs
        aadhar_error = {}

        if Student.objects.filter(aadhar_number=aadhar_number).exists():
            aadhar_error["aadhar_error"] = True

        if aadhar_error:
            messages.error(request, "The Aadhar Card number is already exists.")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **aadhar_error  # Pass error indicators
            })
        
        # Display the error message if the EMIS number error occurs
        emis_error = {}

        if Student.objects.filter(emis_number=emis_number).exists():
            emis_error["emis_error"] = True

        if emis_error:
            messages.error(request, "The EMIS number is already exists.")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **emis_error  # Pass error indicators
            })
        
        # Display the error message if the SSLC mark error occurs
        sslc_error = {}

        if not sslc_mark:
            sslc_error["sslc_error"] = True

        if sslc_error:
            messages.error(request, "Please Enter your SSLC Mark!")

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'religion': religion,
                'community': community,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'emis_number': emis_number,
                'hosteller': hosteller,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'aadhar_number': aadhar_number,
                'father_name': father_name,
                'mother_name': mother_name,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'father_occupation': father_occupation,
                'single_parent': single_parent,
                'first_graduate': first_graduate,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                **sslc_error  # Pass error indicators
            })
        
        # It will set the value as No if the user does not give the value
        if not govt_school:
            govt_school = 'No'

        # It will set the value as No if the user does not give the value
        if not first_graduate:
            first_graduate = 'No'

        # It will set the value as No if the user does not give the value
        if not hosteller:
            hosteller = 'No'

        # It will set the value as No if the user does not give the value
        if not single_parent:
            single_parent = 'No'
        
        # To store the given input value into the users_student tabel
        Student.objects.create(
            first_name = first_name if first_name else None,
            last_name = last_name if last_name else None,
            dob = dob if dob else None,
            gender = gender if gender else None,
            blood_group = blood_group if blood_group else None,
            mother_tongue = mother_tongue if mother_tongue else None,
            differently_abled = differently_abled if differently_abled else None,
            religion = religion if religion else None,
            community = community if community else None,
            reg_no = reg_no if reg_no else None,
            program_name = program_name if program_name else None,
            program_type = program_type if program_type else None,
            year_of_joining = year_of_joining if year_of_joining else None,
            mentor_name = mentor_name if mentor_name else None,
            sslc_mark = sslc_mark if sslc_mark else None,
            hsc_iti_mark = hsc_iti_mark if hsc_iti_mark else None,
            govt_school = govt_school if govt_school else None,
            emis_number = emis_number if emis_number else None,
            hosteller = hosteller if hosteller else None,
            extra_curricular = extra_curricular if extra_curricular.strip() else None,
            achievements = achievements if achievements.strip() else None,
            aadhar_number = aadhar_number if aadhar_number else None,
            father_name = father_name if father_name else None,
            mother_name = mother_name if mother_name else None,
            mobile_father = mobile_father if mobile_father else None,
            mobile_mother = mobile_mother if mobile_mother else None,
            mobile_sibling = mobile_sibling if mobile_sibling else None,
            mobile_guardian = mobile_guardian if mobile_guardian else None,
            father_occupation = father_occupation if father_occupation else None,
            single_parent = single_parent if single_parent else None,
            first_graduate = first_graduate if first_graduate else None,
            email = email if email else None,
            address = address if address else None,
            district = district if district else None,
            pin_code = pin_code if pin_code else None,
            bank_name = bank_name if bank_name else None,
            branch_name = branch_name if branch_name else None,
            account_number = account_number if account_number else None,
            ifsc_code = ifsc_code if ifsc_code else None,
        )

        messages.success(request, "Student' s data stored successfully!")
        return redirect('users:add_stu')

    return render(request, "users/add_stu.html", context)

# To render the View Student page
# Only logged-in users can access this page
def view_stu(request):
    user = request.user

    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return redirect('home:index')

    if user.is_superuser:
        students = Student.objects.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).order_by(Lower('full_name')) #case insensitive sort
    else:
        students = Student.objects.filter(mentor_name=user.first_name).annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).order_by(Lower('full_name')) # case insensitive sort

    return render(request, 'users/view_stu.html', {'students': students})

# To retrieve the student data imediatly when the user starts to search (Live filter)
# It will be render in the same view_stu.html page
def view_stu_ajax(request):
    user = request.user

    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return render(request, 'home/index.html')

    search_term = request.GET.get('search', '').strip()

    if search_term:
        if search_term.isdigit():
            students = Student.objects.filter(reg_no__startswith = search_term)
        else:
            students = Student.objects.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(reg_no__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(program_name__icontains=search_term) |
                Q(mentor_name__icontains=search_term)
            )

    else:
        if user.is_superuser:
            students = Student.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).order_by(Lower('full_name')) #case insensitive sort
        else:
            students = Student.objects.filter(mentor_name=user.first_name).annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).order_by(Lower('full_name')) # case insensitive sort

    return render(request, 'users/student_table_rows.html', {'students': students})

def upload_stu(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']

        try:
            # Load Excel file into a DataFrame
            df = pd.read_excel(excel_file)

            # Clean whitespace
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # Convert NaN (float) to None
            df = df.where(pd.notnull(df), None)

            # Extra: Convert "nan", "NaN", or empty strings ("") to None
            df = df.applymap(lambda x: None if str(x).strip().lower() in ['nan', ''] else x)

            # Set default value "No" for specific fields if they are empty
            default_no_fields = ['Studied in Govt. School', 'First Graduate', 'Hosteller', 'Single Parent', 'Differently abled']
            
            for field in default_no_fields:
                df[field] = df[field].apply(lambda x: x if x not in [None, '', 'nan', 'NaN'] else 'No')

            # Loop through rows and save to DB
            for index, row in df.iterrows():
                Student.objects.create(
                    first_name = row['First Name'],
                    last_name = row['Last Name'],
                    dob = row['Date of Birth'],
                    gender = row['Gender'],
                    blood_group = row['Blood Group'],
                    mother_tongue = row['Mother Tongue'],
                    differently_abled = row['Differently abled'],
                    religion = row['Religion'],
                    community = row['Community'],
                    reg_no = row['Register number'],
                    program_name = row['Program Name'],
                    program_type = row['Program Type'],
                    year_of_joining = row['Year of Joining'],
                    mentor_name = row['Name of the Mentor'],
                    sslc_mark = row['SSLC Mark'],
                    hsc_iti_mark = row['HSC/ITI Mark'],
                    govt_school = row['Studied in Govt. School'],
                    emis_number = row['EMIS Number'],
                    hosteller = row['Hosteller'],
                    extra_curricular = row['Extra Curricular (Optional)'],
                    achievements = row['Any achievements (Optional)'],
                    aadhar_number = row['Aadhar Card Number'],
                    father_name = row['Father Name'],
                    mother_name = row['Mother Name'],
                    mobile_father = row['Mobile Number - Father'],
                    mobile_mother = row['Mobile Number - Mother'],
                    mobile_sibling = row['Mobile Number - Sibling (Optional)'],
                    mobile_guardian = row['Mobile Number - Guardian (Optional)'],
                    father_occupation = row['Father Occupation'],
                    single_parent = row['Single Parent'],
                    first_graduate = row['First Graduate'],
                    email = row['E-Mail ID'],
                    address = row['Address'],
                    district = row['District'],
                    pin_code = row['PIN Code'],
                    bank_name = row['Name of the Bank'],
                    branch_name = row['Branch Name'],
                    account_number = row['Account Number'],
                    ifsc_code = row['IFSC Code'],
                    # add all other fields from your model
                )

            messages.success(request, "Students uploaded successfully.")
            return redirect('users:upload_stu')  # replace with actual URL name

        except Exception as e:
            messages.error(request, f"Error uploading file: {str(e)}")
            return redirect('users:upload_stu')  # replace with actual URL name

    return render(request, 'users/upload_stu.html')  # fallback GET request

def download_stu_format(request):
    """
    Downloads the student format as an Excel (.xlsx) file.
    """
    try:
        headers = ['Student ID', 'Name', 'Class', 'Major']
        df = pd.DataFrame(columns=headers)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='StudentFormat', index=False)

        output.seek(0)
        file_data = output.getvalue()

        response = HttpResponse(
            file_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="student_format.xlsx"'
        return response
    except Exception as e:
        print(f"Error in download_stu_format: {str(e)}")
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


# To render the Edit Student page
# Only logged-in users can access this page
def edit_student(request, aadhar_number):
    student = get_object_or_404(Student, aadhar_number=aadhar_number)
    
    if request.method == "POST":
        # Helper function to handle empty values
        def clean_input(value):
            return value.strip() if value and value.strip() else None

        # Personal Details
        student.first_name = clean_input(request.POST.get("first_name"))
        student.last_name = clean_input(request.POST.get("last_name"))
        student.dob = parse_date(request.POST.get("dob")) or None
        student.gender = clean_input(request.POST.get("gender"))
        student.blood_group = clean_input(request.POST.get("blood_group"))
        student.mother_tongue = clean_input(request.POST.get("mother_tongue"))
        student.differently_abled = clean_input(request.POST.get("differently_abled"))
        student.religion = clean_input(request.POST.get("religion"))
        student.community = clean_input(request.POST.get("community"))

        # Educational Details
        student.reg_no = clean_input(request.POST.get("reg_no"))
        student.program_name = clean_input(request.POST.get("program_name"))
        student.program_type = clean_input(request.POST.get("program_type"))
        student.year_of_joining = parse_date(request.POST.get("year_of_joining")) or None
        student.mentor_name = clean_input(request.POST.get("mentor_name"))
        student.sslc_mark = clean_input(request.POST.get("sslc_mark"))
        student.hsc_iti_mark = clean_input(request.POST.get("hsc_iti_mark"))
        student.govt_school = clean_input(request.POST.get("govt_school"))
        student.emis_number = clean_input(request.POST.get("emis_number"))
        student.hosteller = clean_input(request.POST.get("hosteller"))
        student.extra_curricular = clean_input(request.POST.get("extra_curricular"))
        student.achievements = clean_input(request.POST.get("achievements"))

        # Identification Details
        student.aadhar_number = clean_input(request.POST.get("aadhar_number"))

        # Family Details
        student.father_name = clean_input(request.POST.get("father_name"))
        student.mother_name = clean_input(request.POST.get("mother_name"))
        student.mobile_father = clean_input(request.POST.get("mobile_father"))
        student.mobile_mother = clean_input(request.POST.get("mobile_mother"))
        student.mobile_sibling = clean_input(request.POST.get("mobile_sibling"))
        student.mobile_guardian = clean_input(request.POST.get("mobile_guardian"))
        student.father_occupation = clean_input(request.POST.get("father_occupation"))
        student.single_parent = clean_input(request.POST.get("single_parent"))
        student.first_graduate = clean_input(request.POST.get("first_graduate"))

        # Contact Details
        student.email = clean_input(request.POST.get("email"))
        student.address = clean_input(request.POST.get("address"))
        student.district = clean_input(request.POST.get("district"))
        student.pin_code = clean_input(request.POST.get("pin_code"))

        # Bank Details
        student.bank_name = clean_input(request.POST.get("bank_name"))
        student.branch_name = clean_input(request.POST.get("branch_name"))
        student.account_number = clean_input(request.POST.get("account_number"))
        student.ifsc_code = clean_input(request.POST.get("ifsc_code"))

        # Save changes
        student.save()
        
        return redirect("users:dashboard")  # Redirect to student dashboard after editing

    return render(request, "users/edit_student.html", {"student": student})

# To render the Student Details page according to the student Aadhar number
# Only logged-in users can access this page
@login_required
def student_detail(request, aadhar_number):
    user = request.user

    # Redirect to home:index if the user is not authenticated
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return redirect('home:index')
    
    """
    View student details based on the given register number.
    """
    student = get_object_or_404(Student, aadhar_number=aadhar_number)
    return render(request, 'users/student_detail.html', {'student': student})

# To delete the student record from the Database according to the student aadhar number
@login_required
def delete_student(request, aadhar_number):
    # Try to find the student by reg_no first, otherwise use first_name
    student = Student.objects.filter(aadhar_number=aadhar_number).first()

    if not student:
        messages.error(request, "Student record not found.")
        return redirect('users:view_stu')  # Redirect if student doesn't exist

    # Check if the logged-in user is the student's mentor
    if student.mentor_name == request.user.first_name:
        student.delete()
        messages.success(request, "Student record deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this student.")

    return redirect('users:view_stu')  # Redirect to the student listing page

# Function to conver the image file into Base64 code
def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except FileNotFoundError:
        return None  # Handle the case where the file doesn't exist

# To download the student details as PDF from the webpage
def download_student_pdf(request, aadhar_number):
    try:
        student = Student.objects.get(aadhar_number=aadhar_number)
        image_path = os.path.join(settings.STATIC_ROOT, 'images/GPT_header_logo.png')
        base64_image = image_to_base64(image_path)
        if base64_image is None:
            return HttpResponse("Image not found", status=404)

        html_content = render_to_string('users/student_detail_pdf.html', {
            'student': student,
            'base64_image': base64_image,
        })

        config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)

        # Configuring the page size (A4 sheet size)
        options = {
            'page-size': 'A4',
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'encoding': 'UTF-8',
            'quiet': '',
            'enable-local-file-access': ''
        }

        pdf = pdfkit.from_string(html_content, False, options=options, configuration=config)
        filename = f"GPTUMCHUB {student.first_name} {student.last_name}.pdf"
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Student.DoesNotExist:
        return HttpResponse("Student not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {e}", status=500)


def resize_image(image, max_size=(500, 500)):
    """Resizes an image if it exceeds the specified maximum dimensions."""
    try:
        if isinstance(image, InMemoryUploadedFile):
            img = Image.open(image)
        else:
            img = Image.open(image)

        width, height = img.size

        if width > max_size[0] or height > max_size[1]:
            img.thumbnail(max_size)

            output = BytesIO()
            img.save(output, format='JPEG', quality=85)
            output.seek(0)

            resized_image = InMemoryUploadedFile(
                output,
                'ImageField',
                image.name,
                'image/jpeg',
                output.tell,
                None
            )

            return resized_image
        else:
            return image
    except Exception as e:
        print(f"Error resizing image: {e}")
        return image

# Function used to Generate and send the 6 digit OTP to users corresponding E-Mail ID
def send_otp(email, request):
    otp = ''.join(random.choices(string.digits, k=6))  # Generate 6-digit OTP
    expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    request.session['otp'] = otp
    request.session['otp_expiry'] = expiry_time.timestamp()

    subject = "Your GPTU MC HUB OTP for Password Change Verification Code"
    from_email = f"GPTU MC HUB <{settings.EMAIL_HOST_USER}>"
    text_content = f"Hello,\n\nYour OTP for password change verification is: {otp}\nThis OTP will expire in 1 minute.\n\nPlease do not share this code with anyone.\n\nRegards,\nGPTU MC HUB Team"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>GPTU MC HUB - OTP for Password Change Verification Code</h2>
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


def my_profile(request):
    
    if request.method == "GET":
        # Only clear if not redirected from OTP generation
        if request.GET.get("otp_sent") != "1":
            for key in ["otp", "otp_expiry", "pending_password", "otp_sent"]:
                request.session.pop(key, None)

    try:
        profile = UserProfile.objects.get(username=request.user.username) # Use the correct relation
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(username=request.user.username) # create if does not exist.

    special_chars = set(string.punctuation)


    #profile = UserProfile.objects.get(username=request.user.username)

    if request.method == "POST":
        if 'update_profile' in request.POST:
            # Helper to clean input
            def clean_input(value):
                return value.strip() if value and value.strip() else None

            profile.first_name = clean_input(request.POST.get("first_name"))
            profile.last_name = clean_input(request.POST.get("last_name"))
            profile.email = clean_input(request.POST.get("email"))
            profile.department = clean_input(request.POST.get("department"))
            profile.gender = clean_input(request.POST.get("gender"))

            profile.save()

        elif 'upload_picture' in request.POST and request.FILES.get("profile_picture"):
            uploaded_image = request.FILES["profile_picture"]
            resized_image = resize_image(uploaded_image)

            if resized_image:
                profile.profile_picture = resized_image
                profile.save()

        elif 'generate_otp' in request.POST:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not old_password or not new_password or not confirm_password:
                messages.error(request, "All password fields are required.", extra_tags='password_form')
                return redirect(reverse("users:my_profile") + "#password-section")

            if not check_password(old_password, profile.password):
                messages.error(request, "Old password is incorrect.", extra_tags='password_form')
                return redirect(reverse("users:my_profile") + "#password-section")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.", extra_tags='password_form')
                return redirect(reverse("users:my_profile") + "#password-section")

            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters.")
                return redirect(reverse("users:my_profile") + "#password-section")
            
            if not any(char in special_chars for char in new_password):
                messages.error(request, 'Password must contain at least one special character!', extra_tags='password_form')
                return redirect(reverse("users:my_profile") + "#password-section")

            # Store new password temporarily in session
            request.session['pending_password'] = new_password

            # Send OTP using your custom function
            send_otp(profile.email, request)
            messages.success(request, "OTP sent successfully to your email ID.", extra_tags='password_form')
            request.session['otp_sent'] = True  # Set the flag in session
            return redirect(reverse("users:my_profile") + "?otp_sent=1#password-section")

        elif 'verify_otp' in request.POST:
            entered_otp = request.POST.get("otp")
            stored_otp = request.session.get("otp")
            expiry_time = request.session.get("otp_expiry")
            new_password = request.session.get("pending_password")

            if expiry_time and datetime.datetime.now().timestamp() > expiry_time:
                messages.error(request, "OTP has expired. Please request a new one.", extra_tags='otp_form')
                return redirect(reverse("users:my_profile") + "#password-section")

            if entered_otp == stored_otp and new_password:
                profile.password = make_password(new_password)
                profile.save()
                # Cleanup
                for key in ["otp", "otp_expiry", "pending_password", "show_otp_modal", "last_otp_sent"]:
                    request.session.pop(key, None)
                messages.success(request, "Password updated successfully.", extra_tags='otp_form')
                request.session.pop('otp_sent', None)
                return redirect("users:my_profile")
            else:
                messages.error(request, "Invalid OTP.", extra_tags='otp_form')
                return redirect(reverse("users:my_profile") + "#password-section")
            
        elif 'resend_otp' in request.POST:
            if request.session.get('otp') and profile.email:

                # Remove Old OTP from Session
                request.session.pop("otp", None)
                request.session.pop("otp_expiry", None)

                # Generate new OTP and expiry
                new_otp = ''.join(random.choices(string.digits, k=6))
                expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                request.session["otp"] = new_otp
                request.session["otp_expiry"] = expiry_time.timestamp()

                # HTML email content (copied from your send_otp style)
                subject = "Your New OTP for GPTU MC HUB Verification"
                from_email = f"GPTU MC HUB <{settings.EMAIL_HOST_USER}>"
                text_content = f"Hello,\n\nYour new OTP for verification is: {new_otp}\nThis OTP will expire in 1 minute.\n\nPlease do not share this code with anyone.\n\nRegards,\nGPTU MC HUB Team"

                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2>GPTU MC HUB - OTP for Password Change Verification Code</h2>
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
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [profile.email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    messages.success(request, "A new OTP has been sent to your email.")
                except smtplib.SMTPException as e:
                    # Log the error internally (e.g., using logging module)
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to send OTP email: {e}")
                    messages.error(request, "Failed to send OTP. Please try again later.")
                return redirect(reverse("users:my_profile") + "#password-section")

            else:
                messages.error(request, "Something went wrong. Please try again.")
                return redirect(reverse("users:my_profile") + "#password-section")

    return render(request, 'users/my_profile.html', {
        'profile': profile,
    })

# To logout from the users profile
def logout(request):
    django_logout(request)  # Django handles session clearing
    return redirect('home:index')


