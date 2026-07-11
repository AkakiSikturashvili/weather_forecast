from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission — მხოლოდ ლოკაციის მფლობელს შეუძლია
    წაშალოს/შეცვალოს ის.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.user_id == request.user.id
        return obj.user_id == request.user.id
