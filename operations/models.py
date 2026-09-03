import secrets
import uuid

from django.conf import settings
from django.db import models

from common.models import SoftDeletedModel


class Client(SoftDeletedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=32, unique=True)
    api_token = models.CharField(max_length=64, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    contact_email = models.EmailField(blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.api_token:
            self.api_token = secrets.token_hex(24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


class WorkOrder(SoftDeletedModel):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    reference = models.CharField(max_length=40, unique=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="work_orders")
    service_type = models.ForeignKey(
        "catalog.ServiceType", on_delete=models.PROTECT, related_name="work_orders"
    )
    status = models.ForeignKey(
        "catalog.WorkOrderStatus", on_delete=models.PROTECT, related_name="work_orders"
    )
    region = models.ForeignKey(
        "catalog.Region", on_delete=models.PROTECT, related_name="work_orders"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    address = models.CharField(max_length=255, blank=True, default="")
    scheduled_for = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_work_orders",
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.reference
