from django.contrib import admin

from .models import PayoutRequest


@admin.register(PayoutRequest)
class PayoutRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "amount", "currency", "status", "maker", "created_at")
    list_filter = ("status", "currency")
