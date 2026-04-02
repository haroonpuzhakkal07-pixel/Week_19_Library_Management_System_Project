from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    # Admins Can Edit, users can only read
    def has_permission(self, request, view):
        # Read-only allowed for everyone
        if request.method in SAFE_METHODS:
            return True
        # Write only for admin
        return request.user and request.user.is_staff