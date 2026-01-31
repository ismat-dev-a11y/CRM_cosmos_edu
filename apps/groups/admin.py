from django.contrib import admin
from django.urls import reverse
from django.db import models
from django import forms

from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import Room, GroupStudent, Group


class GroupStudentInline(TabularInline):
    model = GroupStudent
    extra = 1
    # autocomplete_fields = ['student']


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ['name', 'capacity_display']
    search_fields = ['name']

    @display(description="Sig'imi", label=True)
    def capacity_display(self, obj):
        return f"{obj.capacity} kishilik"


@admin.register(GroupStudent)
class GroupStudentAdmin(ModelAdmin):
    list_display = ['student', 'group', 'status_label', 'joined_at']
    list_filter = ['status', 'group']
    search_fields = ['student__username', 'group__name']

    @display(
        description="Status",
        label={
            "ACTIVE": "success",
            "FROZEN": "info",
            "LEFT": "danger",
        }
    )
    def status_label(self, obj):
        return obj.get_status_display()


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    # 🔑 MUHIM FIX — TimeField uchun
    formfield_overrides = {
        models.TimeField: {
            "widget": forms.TimeInput(format="%H:%M")
        }
    }

    list_display = [
        'id',
        'name',
        'course_link',
        'mentor',
        'lesson_time',
        'status_badge',
        'student_count'
    ]

    list_filter = ['status', 'course']
    search_fields = ['name', 'mentor__username']
    inlines = [GroupStudentInline]

    fieldsets = (
        ("Asosiy Ma'lumotlar", {
            "fields": (("name", "status"), ("course", "mentor"), "room")
        }),
        ("Dars Jadvali", {
            "fields": (("lesson_days", "start_time", "end_time"),
                       ("start_date", "end_date"))
        }),
        ("Cheklovlar", {
            "fields": ("max_students",),
        }),
    )

    @display(description="Kurs", header=True)
    def course_link(self, obj):
        url = reverse("admin:courses_course_change", args=[obj.course.id])
        return (obj.course.title, url)

    @display(description="Vaqti")
    def lesson_time(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"

    @display(
        description="Status",
        label={
            "ACTIVE": "success",
            "WAITING": "warning",
            "FINISHED": "secondary",
        }
    )
    def status_badge(self, obj):
        return obj.status

    @display(description="O'quvchilar")
    def student_count(self, obj):
        return f"{obj.students.count()}/{obj.max_students}"
