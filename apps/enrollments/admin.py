from django.contrib import admin
from .models import Enrollment, Attendance, Assignment
from unfold.admin import ModelAdmin
@admin.register(Enrollment)
class EnrollmentAdmin(ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_active', 'is_paid')
    list_filter = ('is_active', 'is_paid', 'course', 'enrolled_at')
    search_fields = ('student__full_name', 'student__email', 'course__title')
    date_hierarchy = 'enrolled_at'
    list_editable = ('is_active', 'is_paid')

@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):
    list_display = ('student', 'lesson', 'status', 'date')
    list_filter = ('status', 'date', 'lesson__course')
    search_fields = ('student__full_name', 'lesson__title')
    date_hierarchy = 'date'
    list_editable = ('status',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'lesson')

@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    list_display = ('id', 'title', 'lesson', 'due_date', 'max_score', 'created_at')
    list_filter = ('due_date', 'lesson__course')
    search_fields = ('title', 'description', 'lesson__title')
    ordering = ('-due_date',)