from rest_framework.permissions import IsAuthenticated


class IsCustomerPermission(IsAuthenticated):
    """
    Custom permission to allow access only to customers.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and not request.user.is_staff
