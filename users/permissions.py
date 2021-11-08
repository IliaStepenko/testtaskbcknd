from rest_framework import permissions


class IsOwnerOrAdminPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
