from django.contrib import admin

from .models import Client, WorkOrder


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active", "created_at")
    search_fields = ("code", "name")
    readonly_fields = ("api_token",)


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ("reference", "client", "status", "region", "assigned_to", "scheduled_for")
    list_filter = ("status", "region", "service_type")
    search_fields = ("reference", "title")
