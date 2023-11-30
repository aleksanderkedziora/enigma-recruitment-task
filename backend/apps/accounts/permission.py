from rest_framework import permissions


class IsStaffOrNotAuthenticated(permissions.BasePermission):
    """
    Custom permission to allow access only to staff or unauthenticated users.
    """

    def has_permission(self, request, view):
        return request.user.is_staff or not request.user.is_authenticated
