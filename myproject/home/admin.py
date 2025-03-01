from django.contrib import admin

# Register your models here.
from .models import UserProfile  # Import the UserProfile model

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'department', 'gender')
    search_fields = ('user_id', 'email')
    list_filter = ('department', 'gender')