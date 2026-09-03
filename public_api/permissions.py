from rest_framework.permissions import BasePermission

from operations.models import Client


class HasClientApiToken(BasePermission):
    """Authenticate partner integrations via `api_token` header."""

    message = "Valid api_token header required."

    def has_permission(self, request, view):
        token = request.headers.get("api_token") or request.headers.get("api-token")
        if not token:
            return False
        client = Client.objects.filter(api_token=token, is_active=True, is_deleted=False).first()
        if not client:
            return False
        request.client = client
        return True
