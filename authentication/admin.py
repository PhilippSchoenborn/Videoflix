"""
Admin configuration for authentication app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerificationToken, PasswordResetToken


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for CustomUser
    """
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_email_verified', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_email_verified', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('is_email_verified', 'date_of_birth', 'profile_image')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name')
        }),
    )


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for EmailVerificationToken
    """
    list_display = ('user', 'token', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'token')
    readonly_fields = ('token', 'created_at')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for PasswordResetToken
    """
    list_display = ('user', 'token', 'used', 'created_at')
    list_filter = ('used', 'created_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('token', 'created_at')
