from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('add-student/', views.add_stu, name='add_stu'),
    path('view-student/', views.view_stu, name='view_stu'),
    path('view/<str:reg_no>/', views.view_student, name='view_student'),
    path('delete/<str:first_name>/', views.delete_student, name='delete_student'),
]