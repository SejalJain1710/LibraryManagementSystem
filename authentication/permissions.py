from rest_framework.permissions import BasePermission

class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.roles.filter(name='librarian').exists()
        return False 

class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.roles.filter(name='member').exists()
