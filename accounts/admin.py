from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import LoginHistory, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "user_type", "client", "is_staff", "is_active")
    list_filter = ("user_type", "is_staff", "is_active")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("FieldOps", {"fields": ("user_type", "client", "phone")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("FieldOps", {"fields": ("user_type", "client", "phone")}),
    )


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "token_active", "ip_address", "created_at")
    list_filter = ("token_active",)
