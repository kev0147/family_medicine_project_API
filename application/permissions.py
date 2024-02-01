from rest_framework.permissions import BasePermission
 
class IsAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
    

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        #return super().has_permission(request, view)
        return bool(request.user.is_staff)
    
class IsPatient(BasePermission):
    def has_permission(self, request, view):
        #return super().has_permission(request, view)
        return bool(request.user.groups.filter(name='patient').exists())
    
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        #return super().has_permission(request, view)
        return bool(request.user.groups.filter(name='doctor').exists())
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        #return super().has_permission(request, view)
        return bool(request.user.groups.filter(name='admin').exists())