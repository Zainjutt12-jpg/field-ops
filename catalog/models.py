from django.db import models

from common.models import SoftDeletedModel


class Region(SoftDeletedModel):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class WorkOrderStatus(SoftDeletedModel):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)
    is_terminal = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "work order statuses"

    def __str__(self):
        return self.name


class ServiceType(SoftDeletedModel):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)
    default_duration_minutes = models.PositiveIntegerField(default=60)

    def __str__(self):
        return self.name
