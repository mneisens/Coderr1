from rest_framework.permissions import BasePermission, IsAdminUser

class IsCustomer(BasePermission):
    """Nur Kunden (type='customer') dürfen Bestellungen erstellen."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.type == 'customer'

class IsBusinessAndOwner(BasePermission):
    """Nur Business-User, wenn sie Eigentümer der Bestellung sind, dürfen Status ändern."""
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.profile.type == 'business'
            and obj.business_user == request.user
        )

# Für DELETE genügt DRF's IsAdminUser
