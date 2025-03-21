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
import os
import pdfkit


"""
Uneccessary import methods

from home.models import UserProfile
from django.contrib.auth.models import User
from django.db import connection

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

        if not first_name:
            messages.error(request, "Please Enter the Name of the student.")

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
            })
        
        if not last_name:
            messages.error(request, "Please Enter the Lastname of the Student.")

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
            })


        reg_no_error = {}

        if Student.objects.filter(reg_no=reg_no).exists():
            reg_no_error["reg_no_error"] = True

        if reg_no_error:
            messages.error(request, "The Register Number is already exists.")

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


def view_stu(request):
    user = request.user

    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return redirect('home:index')

    logged_in_user = request.user
    students = Student.objects.filter(mentor_name=logged_in_user.first_name)

    return render(request, 'users/view_stu.html', {'students': students, 'search_made': False})

def view_stu_ajax(request):
    user = request.user

    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return render(request, 'home/index.html')

    search_term = request.GET.get('search', '').strip()
    logged_in_user = request.user

    if search_term:
        if search_term.isdigit():
            students = Student.objects.filter(reg_no=search_term)
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


def download_student_pdf(request, aadhar_number):
    student = Student.objects.get(aadhar_number=aadhar_number)

    # Render your student_detail.html content to HTML string
    html_content = render_to_string('users/student_detail.html', {'student': student})

    config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    # PDFKit options (for A4 size & quality)
    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
        'quiet': ''
    }

    # Path to your CSS file (give full absolute path)
    css_path = r'C:\\Users\\Vignesh Thilagaraj\\OneDrive\\Desktop\\empty\\gptu_mchub\\myproject\\static\\css\\style.css'

    # Generate PDF with HTML + CSS
    pdf = pdfkit.from_string(html_content, False, options=options, configuration=config, css=css_path)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="GPTUMCHUB Student.pdf"'
    return response


def logout(request):
    django_logout(request)  # Django handles session clearing
    return redirect('home:index')
