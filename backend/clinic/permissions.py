from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'doctor'

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'patient'

class IsOwnerDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        return obj.doctor == request.user
