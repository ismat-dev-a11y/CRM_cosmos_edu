from django.contrib import admin
from .models import Course, Lesson
from unfold.admin import ModelAdmin


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ["id", "title", "level", "image"]


@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ["id", "course"]
