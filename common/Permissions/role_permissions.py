from rest_framework.permissions import BasePermission

from accounts.models import UserType


class IsAdminUserType(BasePermission):
    message = "Admin portal access required."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.user_type == UserType.ADMIN)


class IsClientUserType(BasePermission):
    message = "Client portal access required."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.user_type == UserType.CLIENT)


class IsFieldUserType(BasePermission):
    message = "Field technician access required."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.user_type == UserType.FIELD)
