from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only to anyone but write/update/delete only to the object's owner.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # For Post and Comment, check attribute 'author'
        return getattr(obj, 'author', None) == request.user