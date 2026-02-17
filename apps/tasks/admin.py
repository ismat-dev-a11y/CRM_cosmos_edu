from django.contrib import admin
from .models import DailyTask
from unfold.admin import ModelAdmin


@admin.register(DailyTask)
class DailyTaskAdmin(ModelAdmin):
    list_display = ["title", "due_date"]
