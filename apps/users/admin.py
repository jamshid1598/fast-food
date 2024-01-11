from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import Users, SMSToken, OTPStatus


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (_('User Info'),
            {'fields': (
                "first_name",
                "last_name",
                "username",
                "phone",
                "email",
                "two_step_password",
            )
        }),
        (_('Status/Groups/Permissions'),
            {'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )

    add_fieldsets = (
        (_("create new user"), {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )

    list_display = (
        'first_name', 'last_name', 'username', 'phone', 'email',
        'two_step_password', 'is_staff', 'is_superuser', 'is_active',
        'last_login', 'updated_at', 'created_at',
    )
    list_filter = (
        'two_step_password', 'is_staff', 'is_superuser', 'is_active',
        'updated_at', 'created_at',
    )
    ordering = (
        'first_name', 'last_name', 'username', 'phone', 'email',
        'two_step_password', 'is_staff', 'is_superuser', 'is_active',
        'updated_at', 'created_at',
    )
    list_display_links = ('first_name', 'last_name', 'username', 'phone', 'email',)
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(Users, UserAdmin)


@admin.register(SMSToken)
class SMSTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at',)
    list_display_links = ('id', 'created_at', 'updated_at',)


@admin.register(OTPStatus)
class OTPStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_id', 'phone', 'status', 'message', 'created_at', 'updated_at')
    list_display_links = ('id', 'message_id', 'phone', 'status', 'message', 'created_at', 'updated_at')
    search_fields = ('phone',)
