from rest_framework.permissions import BasePermission, SAFE_METHODS

# isAdmin Permission
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'