from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("iCloud Bilgileri", {"fields": ("icloud_email", "icloud_password")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
