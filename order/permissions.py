# orders/permissions.py
from rest_framework.permissions import BasePermission

class IsOrderOwner(BasePermission):
    """
    Custom permission to only allow owners of an order to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the order
        return obj.user == request.user