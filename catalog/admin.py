from django.contrib import admin

from .models import Region, ServiceType, WorkOrderStatus


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_deleted", "created_at")
    search_fields = ("code", "name")


@admin.register(WorkOrderStatus)
class WorkOrderStatusAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_terminal", "sort_order")
    ordering = ("sort_order",)


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "default_duration_minutes")
