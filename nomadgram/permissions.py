from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    해당 객체의 작성자만 업데이트가 가능하다.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            request.user == obj
        )
