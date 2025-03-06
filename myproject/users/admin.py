from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'first_name', 'last_name', 'email', 'program_name', 'year_of_joining')
    search_fields = ('reg_no', 'first_name', 'last_name', 'email')
    list_filter = ('program_name', 'year_of_joining', 'gender', 'community', 'blood_group')

    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'reg_no', 'email', 'dob', 'gender', 'blood_group')
        }),
        ('Program Details', {
            'fields': ('program_name', 'program_type', 'year_of_joining', 'mentor_name')
        }),
        ('Family Details', {
            'fields': ('father_name', 'mother_name', 'mobile_father', 'mobile_mother', 'mobile_guardian', 'single_parent')
        }),
        ('Address & Contact', {
            'fields': ('address', 'district', 'pin_code')
        }),
        ('Academics & Extra', {
            'fields': ('sslc_mark', 'hsc_iti_mark', 'govt_school', 'first_graduate', 'hosteller', 'extra_curricular', 'achievements')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'branch_name', 'account_number', 'ifsc_code')
        }),
    )
