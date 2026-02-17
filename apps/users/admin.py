from django.contrib import admin
from .models import UserProfile
from unfold.admin import ModelAdmin


@admin.register(UserProfile)
class UserAdmin(ModelAdmin):
    list_display = ("id", "phone_number", "role", "is_staff")
    list_filter = ("role",)
    search_fields = ("phone_number", "username__icontains", "email__icontains")

    def is_admin(self, user):
        return user.is_authenticated and (
            user.is_superuser or user.role in ["BOSS", "ADMIN"]
        )

    def has_add_permission(self, request):
        return self.is_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return self.is_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == "BOSS"
        )
