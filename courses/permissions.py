from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'Вы не являетесь владельцем этого курса/урока.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsNotModerator(BasePermission):
    message = 'Вы являетесь модератором'

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Модераторы').exists():
            return False
        return True
