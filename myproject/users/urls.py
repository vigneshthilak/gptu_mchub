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
    path('delete/<str:aadhar_number>/', views.delete_student, name='delete_student'),
    path('my-profile/', views.my_profile, name='my_profile'),
]