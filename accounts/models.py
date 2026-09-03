from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel


class UserType(models.TextChoices):
    ADMIN = "admin", "Admin"
    CLIENT = "client", "Client"
    FIELD = "field", "Field Technician"


class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.ADMIN)
    client = models.ForeignKey(
        "operations.Client",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    phone = models.CharField(max_length=32, blank=True, default="")

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class LoginHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_history")
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, default="")
    token_active = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True, default="")

    class Meta:
        ordering = ["-created_at"]
