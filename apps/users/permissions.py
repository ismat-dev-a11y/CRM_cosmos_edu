from rest_framework.permissions import BasePermission


class IsAuthenticatedAndActive(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active


class IsBoss(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "BOSS"


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["ADMIN", "BOSS"]


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "MENTOR"


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "STUDENT"


class IsMentorOfStudent(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == "MENTOR" and obj.mentor == request.user


class IsAdminOrIsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "ADMIN",
            "MENTOR",
        ]


class CanBeStudent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "STUDENT"
            and request.method in ("GET", "HEAD", "OPTIONS")
        )
