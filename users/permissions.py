from rest_framework import permissions

class IsCandidate(permissions.IsAuthenticated):
    """
    Permissions to allow Candidates
    """

    def has_permission(self, req, view):
        user = req.user
        if(not hasattr(user,'role')):
            return False
        role = user.role
        if(role == 'ROLE_USER' or role == 'ROLE_HR' or role == 'ROLE_ADMIN'):
            return True
        
        return False

class IsHr(permissions.IsAuthenticated):
    """
    Permissions to allow HR of company
    """

    def has_permission(self, req, view):
        user = req.user
        if(not hasattr(user,'role')):
            return False
        role = user.role
        if(role == 'ROLE_HR' or role == 'ROLE_ADMIN'):
            return True
        
        return False

class IsAdmin(permissions.IsAuthenticated):
    """
    Permissions to allow Admin of Company
    """

    def has_permission(self, req, view):
        user = req.user
        if(not hasattr(user,'role')):
            return False
        role = user.role
        if(role == 'ROLE_ADMIN'):
            return True
        
        return False