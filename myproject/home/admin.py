from django.contrib import admin
from .models import UserProfile
from .models import AuthUser
from .models import PasswordResetToken

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'department', 'gender')
    search_fields = ('user_id', 'email')
    list_filter = ('department', 'gender')

@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email')
    search_fields = ('user_id', 'email')
    ordering = ('user_id',)

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    search_fields = ('user__email', 'token')
    list_filter = ('created_at',)
