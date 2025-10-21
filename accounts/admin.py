from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model (WhatsApp OTP based)."""

    list_display = ('phone_number', 'first_name', 'last_name', 'kyc_level', 'score', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'kyc_level')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Lending Info'), {
            'fields': ('kyc_level', 'score', 'aid_recipient'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('phone_number',)
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(User, UserAdmin)
