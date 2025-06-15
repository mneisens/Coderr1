from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBusinessAndOwner(BasePermission):
    """
    Nur Business-User (profile.type='business') dürfen Offers erstellen,
    und nur deren Ersteller dürfen ändern/löschen.
    """
    def has_permission(self, request, view):
        # für CREATE
        if view.action == 'create':
            return (
                request.user.is_authenticated and
                request.user.profile.type == 'business'
            )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Lesen für alle Auth-User
        if request.method in SAFE_METHODS:
            return True
        # Update/Delete nur für Owner
        return obj.user == request.user
