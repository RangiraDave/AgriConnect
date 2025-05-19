from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read operations for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
            
        # Allow write operations for owners and admins
        return obj.owner == request.user or request.user.is_staff

class IsProfileOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow profile owners or admins to edit profiles.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read operations for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
            
        # Allow write operations for profile owners and admins
        return obj.user == request.user or request.user.is_staff

class IsRatingOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow rating owners or admins to edit ratings.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read operations for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
            
        # Allow write operations for rating owners and admins
        return obj.user == request.user or request.user.is_staff

class IsLocationAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access location data.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff 