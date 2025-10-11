from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('add-student/', views.add_stu, name='add_stu'),
    path('view-student/', views.view_stu, name='view_stu'),
    path('view_stu_ajax/', views.view_stu_ajax, name='view_stu_ajax'),
    path('upload-student/', views.upload_stu, name='upload_stu'),
    path('upload-student/', views.download_stu_format, name='download_stu_format'),
    path('student-details/<str:aadhar_number>/', views.student_detail, name='student_detail'),
    path('student/pdf/<str:aadhar_number>/', views.download_student_pdf, name='download_student_pdf'),
    path("edit-student/<str:aadhar_number>/", views.edit_student, name="edit_student"),
    path('upload-student-mark', views.upload_stu_mark, name='upload_stu_mark'),
    path('upload-sslc-mark', views.upload_sslc_mark, name='upload_sslc_mark'),
    path('upload-hsc-mark', views.upload_hsc_mark, name='upload_hsc_mark'),
    path('upload-iti-mark', views.upload_iti_mark, name='upload_iti_mark'),
    path('upload-college-marks', views.upload_college_marks, name='upload_college_marks'),
    path('delete/<str:aadhar_number>/', views.delete_student, name='delete_student'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
]