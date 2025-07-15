"""
Admin configuration for authentication app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerificationToken, PasswordResetToken
from .utils import create_verification_token


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
    # Felder sind jetzt editierbar, damit Admin-Aktion funktioniert
    # readonly_fields = ('is_active', 'is_email_verified')
    actions = ["activate_and_verify_users"]

    def save_model(self, request, obj, form, change):
        # Erzwinge is_active und is_email_verified auf False beim Anlegen
        if not change:
            obj.is_active = False
            obj.is_email_verified = False
            super().save_model(request, obj, form, change)
            # Token nach dem Speichern generieren
            create_verification_token(obj)
        else:
            super().save_model(request, obj, form, change)

    @admin.action(description="User aktivieren und verifizieren")
    def activate_and_verify_users(self, request, queryset):
        for user in queryset:
            user.is_active = True
            user.is_email_verified = True
            user.save()
        self.message_user(request, "Ausgewählte User wurden aktiviert und verifiziert.")


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
