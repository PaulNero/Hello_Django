
from rest_framework.permissions import BasePermission, SAFE_METHODS

# Пример кастомных разрешений

class IsReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user and obj.author == request.user
    
class IsOwnerOrStaff(BasePermission):
    """
    Разрешает доступ только владельцу профиля или администратору.
    Используется в app_users.api.view => ProfileRUDView
    """
    def has_object_permission(self, request, view, obj):
        if request.method == SAFE_METHODS:
            return True
        
        return obj == request.user or request.user.is_staff
