from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as django_logout 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Student
from django.contrib.auth.models import AnonymousUser
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import pdfkit
import os
import base64

"""
Uneccessary import methods

from home.models import UserProfile
from django.contrib.auth.models import User
from django.db import connection
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


"""

@login_required(login_url='/')  # Ensures only logged-in users can access the dashboard
@cache_control(no_store=True, no_cache=True, must_revalidate=True)  # Prevents browser from storing dashboard page
def dashboard(request):
    user = request.user  # Fetch authenticated user

    context = {
        "mentor_first_name": user.first_name,
        "mentor_last_name": user.last_name,
        "mentor_department": user.department,
        "mentor_gender": user.gender,
    }

    return render(request, "users/dashboard.html", context)

def add_stu(request):
    user = request.user

    # Redirect to home:index if the user is not authenticated
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return redirect('home:index')

    context = {
        "mentor_name": user.first_name,
    }

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

        if not differently_abled:
            differently_abled = 'No'

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
        
        if not govt_school:
            govt_school = 'No'

        if not first_graduate:
            first_graduate = 'No'

        if not hosteller:
            hosteller = 'No'

        if not single_parent:
            single_parent = 'No'
        
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


def view_stu(request):
    user = request.user

    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return redirect('home:index')

    logged_in_user = request.user
    students = Student.objects.filter(mentor_name=logged_in_user.first_name)

    return render(request, 'users/view_stu.html', {'students': students})

def view_stu_ajax(request):
    user = request.user

    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return render(request, 'home/index.html')

    search_term = request.GET.get('search', '').strip()
    logged_in_user = request.user

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
        students = Student.objects.filter(mentor_name=logged_in_user.first_name)

    return render(request, 'users/student_table_rows.html', {'students': students})

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


def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except FileNotFoundError:
        return None  # Handle the case where the file doesn't exist

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


def logout(request):
    django_logout(request)  # Django handles session clearing
    return redirect('home:index')


