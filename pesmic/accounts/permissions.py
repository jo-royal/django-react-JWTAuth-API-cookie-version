from rest_framework import permissions


#allow only owner to read and write
class IsUser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
    


class IsBrandActive(permissions.BasePermission):
    #give only permission to brand active users
    def has_permission(self, request, view):
        return request.user.is_brandowner 
    


class BrandOwner(permissions.BasePermission):
    #check if is brandowner
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
