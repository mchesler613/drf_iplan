from rest_framework import permissions

class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the authenticated user to edit their profile.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the authenticated user who owns their user profile
        if request.user.is_authenticated:
            return obj == request.user 
        else:
            return False


class IsPersonOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the person who's also authenticated to edit
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the authenticated user who's also the person
        print(obj.user, request.user)
        if request.user.is_authenticated:
            return obj.user == request.user
        else:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the person who created the task to edit it
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to person who created the task
        if request.user.is_authenticated:
            return obj.person == request.user.person
        else:
            return False


class IsCreatedByOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the person who created the task to edit it
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to person who created the task
        if request.user.is_authenticated:
            return obj.created_by == request.user.person
        else:
            return False

