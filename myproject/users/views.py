from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout 
from django.contrib.auth.decorators import login_required
from .models import Student

"""
Uneccessary import methods

from home.models import UserProfile
from django.contrib.auth.models import User
from django.db import connection

"""

@login_required  # Ensures only logged-in users can access the dashboard

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
    
    if user == False:
        return redirect('home:index')

    context = {
        "first_name": user.first_name,
    }

    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name") or None
        reg_no = request.POST.get("reg_no")
        program_name = request.POST.get("program_name") or None
        program_type = request.POST.get("program_type") or None
        year_of_joining = request.POST.get("year_of_joining") or None
        mentor_name = request.POST.get("mentor_name") or None
        father_name = request.POST.get("father_name") or None
        mother_name = request.POST.get("mother_name") or None
        dob = request.POST.get("dob") or None
        gender = request.POST.get("gender") or None
        blood_group = request.POST.get("blood_group") or None
        mother_tongue = request.POST.get("mother_tongue") or None
        differently_abled = request.POST.get("differently_abled") or None
        mobile_father = request.POST.get("mobile_father") or None
        mobile_mother = request.POST.get("mobile_mother") or None
        mobile_sibling = request.POST.get("mobile_sibling") or None
        mobile_guardian = request.POST.get("mobile_guardian") or None
        email = request.POST.get("email") or None
        address = request.POST.get("address") or None
        district = request.POST.get("district") or None
        pin_code = request.POST.get("pin_code") or None
        father_occupation = request.POST.get("father_occupation") or None
        aadhar_number = request.POST.get("aadhar_number") or None
        emis_number = request.POST.get("emis_number") or None
        sslc_mark = request.POST.get("sslc_mark") or None
        hsc_iti_mark = request.POST.get("hsc_iti_mark") or None
        govt_school = request.POST.get("govt_school") or None
        first_graduate = request.POST.get("first_graduate") or None
        hosteller = request.POST.get("hosteller") or None
        single_parent = request.POST.get("single_parent") or None
        bank_name = request.POST.get("bank_name") or None
        branch_name = request.POST.get("branch_name") or None
        account_number = request.POST.get("account_number") or None
        ifsc_code = request.POST.get("ifsc_code") or None
        extra_curricular = request.POST.get("extra_curricular") or None
        achievements = request.POST.get("achievements") or None
        religion = request.POST.get("religion") or None
        community = request.POST.get("community") or None

        Student.objects.create(
            first_name = first_name,
            last_name = last_name,
            reg_no = reg_no,
            program_name = program_name,
            program_type = program_type,
            year_of_joining = year_of_joining,
            mentor_name = mentor_name,
            father_name = father_name,
            mother_name = mother_name,
            dob = dob,
            gender = gender,
            blood_group = blood_group,
            mother_tongue = mother_tongue,
            differently_abled = differently_abled,
            mobile_father = mobile_father,
            mobile_mother = mobile_mother,
            mobile_sibling = mobile_sibling,
            mobile_guardian = mobile_guardian,
            email = email,
            address = address,
            district = district,
            pin_code = pin_code,
            father_occupation = father_occupation,
            aadhar_number = aadhar_number,
            emis_number = emis_number,
            sslc_mark = sslc_mark,
            hsc_iti_mark = hsc_iti_mark,
            govt_school = govt_school,
            first_graduate = first_graduate,
            hosteller = hosteller,
            single_parent = single_parent,
            bank_name = bank_name,
            branch_name = branch_name,
            account_number = account_number,
            ifsc_code = ifsc_code,
            extra_curricular = extra_curricular,
            achievements = achievements,
            religion = religion,
            community = community,
        )

        return redirect('users:add_stu')


    return render(request, "users/add_stu.html", context)


def logout(request):
    django_logout(request)  # Django handles session clearing
    return redirect('home:index')
