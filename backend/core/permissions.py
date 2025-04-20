from rest_framework.permissions import BasePermission

class IsMedecin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Médecin').exists()

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Patient').exists()