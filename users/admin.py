from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number', 'profile_image'
            )
        }),
        (_('Roles and Permissions'), {
            'fields': (
                'role', 'is_verified', 'verification_date',
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        (_('Preferences'), {
            'fields': (
                'preferred_language', 'reduced_data_mode',
                'email_notifications', 'push_notifications', 'sms_notifications'
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'role', 'first_name', 'last_name', 'phone_number'
            ),
        }),
    )
    
    list_display = [
        'username', 'email', 'role', 'is_verified', 'is_active',
        'preferred_language', 'created_at'
    ]
    list_filter = [
        'role', 'is_verified', 'is_active', 'preferred_language',
        'email_notifications', 'push_notifications', 'reduced_data_mode'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'verification_date']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('seller_profile')