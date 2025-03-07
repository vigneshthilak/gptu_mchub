from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as django_logout 
from django.contrib.auth.decorators import login_required
from .models import Student
from django.contrib.auth.models import AnonymousUser
from django.utils.dateparse import parse_date

"""
Uneccessary import methods

from home.models import UserProfile
from django.contrib.auth.models import User
from django.db import connection

"""

@login_required(login_url='/')  # Ensures only logged-in users can access the dashboard

def dashboard(request):
    user = request.user  # Fetch authenticated user

    context = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "department": user.department,
        "gender": user.gender,
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
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name") 
        reg_no = request.POST.get("reg_no")
        program_name = request.POST.get("program_name") 
        program_type = request.POST.get("program_type") 
        year_of_joining = parse_date(request.POST.get("year_of_joining"))
        mentor_name = request.POST.get("mentor_name") 
        father_name = request.POST.get("father_name") 
        mother_name = request.POST.get("mother_name") 
        dob = parse_date(request.POST.get("dob")) 
        gender = request.POST.get("gender") 
        blood_group = request.POST.get("blood_group") 
        mother_tongue = request.POST.get("mother_tongue") 
        differently_abled = request.POST.get("differently_abled") 
        mobile_father = request.POST.get("mobile_father") 
        mobile_mother = request.POST.get("mobile_mother") 
        mobile_sibling = request.POST.get("mobile_sibling") 
        mobile_guardian = request.POST.get("mobile_guardian") 
        email = request.POST.get("email") 
        address = request.POST.get("address") 
        district = request.POST.get("district") 
        pin_code = request.POST.get("pin_code") 
        father_occupation = request.POST.get("father_occupation") 
        aadhar_number = request.POST.get("aadhar_number") 
        emis_number = request.POST.get("emis_number") 
        sslc_mark = request.POST.get("sslc_mark") 
        hsc_iti_mark = request.POST.get("hsc_iti_mark") 
        govt_school = request.POST.get("govt_school") 
        first_graduate = request.POST.get("first_graduate") 
        hosteller = request.POST.get("hosteller") 
        single_parent = request.POST.get("single_parent") 
        bank_name = request.POST.get("bank_name") 
        branch_name = request.POST.get("branch_name") 
        account_number = request.POST.get("account_number") 
        ifsc_code = request.POST.get("ifsc_code") 
        extra_curricular = request.POST.get("extra_curricular") 
        achievements = request.POST.get("achievements") 
        religion = request.POST.get("religion") 
        community = request.POST.get("community") 
        
        if program_type == None or program_name == None:
            program_type = False
            program_name = False
            print(f'{program_name}\n{program_type}')
            messages.error(request, "Please select the Program Name & Program Type.")

            error_fields = {
                'program_name_error': program_name,
                'program_type_error': program_type,
            }

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'father_name': father_name,
                'mother_name': mother_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'father_occupation': father_occupation,
                'aadhar_number': aadhar_number,
                'emis_number': emis_number,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'first_graduate': first_graduate,
                'hosteller': hosteller,
                'single_parent': single_parent,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'religion': religion,
                'community': community,
                **error_fields  # Pass error indicators
            })
        
        if not gender:
            print(gender)
            messages.error(request, "Pleases select the Gender.")

            error_fields = {
                'gender_error': gender,
            }

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'father_name': father_name,
                'mother_name': mother_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'father_occupation': father_occupation,
                'aadhar_number': aadhar_number,
                'emis_number': emis_number,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'first_graduate': first_graduate,
                'hosteller': hosteller,
                'single_parent': single_parent,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'religion': religion,
                'community': community,
                **error_fields  # Pass error indicators
            })

        reg_no_exists = Student.objects.filter(reg_no=reg_no).exists()
        email_exists = Student.objects.filter(email=email).exists()
        aadhar_number_exists = Student.objects.filter(aadhar_number=aadhar_number).exists()
        emis_number_exists = Student.objects.filter(emis_number=emis_number).exists()

        if reg_no_exists or email_exists or aadhar_number_exists or emis_number_exists:
            messages.error(request, "Some data already exists.")

            error_fields = {
                'reg_no_error': reg_no_exists,
                'email_error': email_exists,
                'aadhar_error': aadhar_number_exists,
                'emis_number_error': emis_number_exists,
            }

            return render(request, 'users/add_stu.html', {
                'first_name': first_name,
                'last_name': last_name,
                'reg_no': reg_no,
                'program_name': program_name,
                'program_type': program_type,
                'year_of_joining': year_of_joining,
                'mentor_name': mentor_name,
                'father_name': father_name,
                'mother_name': mother_name,
                'dob': dob,
                'gender': gender,
                'blood_group': blood_group,
                'mother_tongue': mother_tongue,
                'differently_abled': differently_abled,
                'mobile_father': mobile_father,
                'mobile_mother': mobile_mother,
                'mobile_sibling': mobile_sibling,
                'mobile_guardian': mobile_guardian,
                'email': email,
                'address': address,
                'district': district,
                'pin_code': pin_code,
                'father_occupation': father_occupation,
                'aadhar_number': aadhar_number,
                'emis_number': emis_number,
                'sslc_mark': sslc_mark,
                'hsc_iti_mark': hsc_iti_mark,
                'govt_school': govt_school,
                'first_graduate': first_graduate,
                'hosteller': hosteller,
                'single_parent': single_parent,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                'extra_curricular': extra_curricular,
                'achievements': achievements,
                'religion': religion,
                'community': community,
                **error_fields  # Pass error indicators
            })
        


        Student.objects.create(
            first_name = first_name if first_name else None,
            last_name = last_name if last_name else None,
            reg_no = reg_no if reg_no else None,
            program_name = program_name if program_name else None,
            program_type = program_type if program_type else None,
            year_of_joining = year_of_joining if year_of_joining else None,
            mentor_name = mentor_name if mentor_name else None,
            father_name = father_name if father_name else None,
            mother_name = mother_name if mother_name else None,
            dob = dob if dob else None,
            gender = gender if gender else None,
            blood_group = blood_group if blood_group else None,
            mother_tongue = mother_tongue if mother_tongue else None,
            differently_abled = differently_abled if differently_abled else None,
            mobile_father = mobile_father if mobile_father else None,
            mobile_mother = mobile_mother if mobile_mother else None,
            mobile_sibling = mobile_sibling if mobile_sibling else None,
            mobile_guardian = mobile_guardian if mobile_guardian else None,
            email = email if email else None,
            address = address if address else None,
            district = district if district else None,
            pin_code = pin_code if pin_code else None,
            father_occupation = father_occupation if father_occupation else None,
            aadhar_number = aadhar_number if aadhar_number else None,
            emis_number = emis_number if emis_number else None,
            sslc_mark = sslc_mark if sslc_mark else None,
            hsc_iti_mark = hsc_iti_mark if hsc_iti_mark else None,
            govt_school = govt_school if govt_school else None,
            first_graduate = first_graduate if first_graduate else None,
            hosteller = hosteller if hosteller else None,
            single_parent = single_parent if single_parent else None,
            bank_name = bank_name if bank_name else None,
            branch_name = branch_name if branch_name else None,
            account_number = account_number if account_number else None,
            ifsc_code = ifsc_code if ifsc_code else None,
            extra_curricular = extra_curricular if extra_curricular else None,
            achievements = achievements if achievements else None,
            religion = religion if religion else None,
            community = community if community else None,
        )

        messages.success(request, "Student' s data stored successfully!")
        return redirect('users:add_stu')


    return render(request, "users/add_stu.html", context)


def logout(request):
    django_logout(request)  # Django handles session clearing
    return redirect('home:index')
