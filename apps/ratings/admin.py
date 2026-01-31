from django.contrib import admin
from .models import Rating
from unfold.admin import ModelAdmin
@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    list_display=['student', 'course', 'score']
    list_filter = ('is_active', )