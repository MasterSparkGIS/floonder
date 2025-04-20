from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("You are not authenticated.")

        if not request.user.is_superuser():
            raise PermissionDenied("You are not authorized to perform this action.")

        return request.user.is_superuser()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            raise PermissionDenied("You are not authenticated.")

        if not request.user.is_superuser:
            raise PermissionDenied("You are not authorized to perform this action.")

        return request.user.is_superuser


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("You are not authenticated.")

        if not request.user.is_admin():
            raise PermissionDenied("You are not authorized to perform this action.")

        return request.user.is_admin()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            raise PermissionDenied("You are not authenticated.")

        if not request.user.is_admin():
            raise PermissionDenied("You are not authorized to perform this action.")

        return request.user.is_admin()


class IsMember(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("You are not authenticated.")

        if not request.user.is_member():
            raise PermissionDenied("You are not authorized to perform this action.")

        return request.user.is_member()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            raise PermissionDenied("You are not authenticated.")

        if not request.user.is_member():
            raise PermissionDenied("You are not authorized to perform this action.")

        return request.user.is_member()
