from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsReviewerOrReadOnly(BasePermission):
    """
    Ersteller darf PATCH/DELETE, jeder Auth-User kann lesen.
    """
    def has_object_permission(self, request, view, obj):
        # Lesen für alle authentifizierten User
        if request.method in SAFE_METHODS:
            return True
        # nur Ersteller darf ändern/löschen
        return obj.reviewer == request.user
