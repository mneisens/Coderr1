from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Nur der Owner darf bearbeiten, alle Auth-User dürfen lesen.
    """
    def has_object_permission(self, request, view, obj):
        # Lesen erlauben für alle authentifizierten User
        if request.method in ('GET',):
            return True
        # Schreiben nur, wenn es das eigene Profil ist
        return obj.user == request.user
