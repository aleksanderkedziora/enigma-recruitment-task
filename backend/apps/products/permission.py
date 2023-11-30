from rest_framework.permissions import IsAuthenticated


class IsStaffPermission(IsAuthenticated):
    """
    Custom permission to allow access only to staff members.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_staff
