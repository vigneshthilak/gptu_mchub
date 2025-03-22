from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'first_name', 'last_name', 'email', 'program_name', 'year_of_joining')
    search_fields = ('reg_no', 'first_name', 'last_name', 'email')
    list_filter = ('program_name', 'year_of_joining', 'gender', 'community', 'blood_group')

    fieldsets = (
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'dob', 'gender', 'blood_group', 'mother_tongue', 'differently_abled', 'religion', 'community')
        }),
        ('Educational Details', {
            'fields': ('reg_no', 'program_name', 'program_type', 'year_of_joining', 'mentor_name', 'sslc_mark', 'hsc_iti_mark', 'govt_school', 'emis_number', 'hosteller', 'extra_curricular', 'achievements')
        }),
        ('Identification Details', {
            'fields': ('aadhar_number',)
        }),
        ('Family Details', {
            'fields': ('father_name', 'mother_name', 'mobile_father', 'mobile_mother', 'mobile_sibling', 'mobile_guardian', 'father_occupation', 'single_parent', 'first_graduate')
        }),
        ('Contact Details', {
            'fields': ('email', 'address', 'district', 'pin_code')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'branch_name', 'account_number', 'ifsc_code')
        }),
    )
