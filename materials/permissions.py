from rest_framework.permissions import BasePermission

from materials.models import Course, Lesson, Subscription, Payment


class IsModarator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Course):
            return obj.author == request.user
        elif isinstance(obj, Lesson):
            return obj.course.author == request.user
        elif isinstance(obj, Payment):
            return obj.user == request.user
        return False


class IsNotStaffUser(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_staff


class IsSubscriber(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Course):
            subscription = Subscription.objects.filter(user=request.user, course=obj.id)
            return subscription.exists()
        elif isinstance(obj, Lesson):
            subscription = Subscription.objects.filter(user=request.user, course=obj.course.id)
            return subscription.exists()
        return False


class IsCustomer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Course):
            purchase = Payment.objects.filter(user=request.user, course=obj.id, status='paid')
            return purchase.exists()
        elif isinstance(obj, Lesson):
            purchase = Payment.objects.filter(user=request.user, lesson=obj.id, status='paid')
            return purchase.exists()
        return False
