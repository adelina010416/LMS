from rest_framework.permissions import BasePermission

from materials.models import Course, Lesson


class IsModarator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Course):
            return obj.author == request.user
        elif isinstance(obj, Lesson):
            return obj.course.author == request.user
        return False


class IsNotStaffUser(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_staff