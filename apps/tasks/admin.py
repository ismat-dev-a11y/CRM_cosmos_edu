from django.contrib import admin
from .models import HomeworkSubmission, HomeworkTask
from unfold.admin import ModelAdmin


@admin.register(HomeworkTask)
class HomeworkTaskAdmin(ModelAdmin):
    list_display = ["group", "title"]

@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(ModelAdmin):
    list_display=['homework_task', 'student']