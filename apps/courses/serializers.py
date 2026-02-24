from rest_framework import serializers
from .models import Course, Lesson
from apps.users.models import UserProfile
from drf_spectacular.utils import extend_schema_field


class LessonSerializer(serializers.ModelSerializer):
    mentor = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.filter(role="MENTOR"),
        required=False,
        allow_null=True,
        help_text="Dars o'tuvchi mentor ID raqami",
    )
    is_completed = serializers.BooleanField(
        read_only=True, help_text="Dars tugatilganmi"
    )

    mentor_name = serializers.SerializerMethodField(
        read_only=True, help_text="Mentor ismi"
    )

    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "mentor",
            "mentor_name",
            "title",
            "day",
            "start_time",
            "end_time",
            "week_number",
            "lesson_type",
            "is_completed",
        ]
        read_only_fields = ["id", "is_completed"]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_mentor_name(self, obj):
        if obj.mentor:
            return obj.mentor.get_full_name() or obj.mentor.username
        return None


class CourseReadSerializers(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Course
        fields = ['title', 'level', 'image']


class CourseCreateSerializer(serializers.ModelSerializer):
    current_students_count = serializers.IntegerField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    image = serializers.ImageField(required=False)  # file upload uchun
    image_url = serializers.URLField(required=False, write_only=True)  # URL uchun

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "level",
            "description",
            "max_students",
            "is_active",
            "price",
            "duration_weeks",
            "image",
            "image_url",
            "created_at",
            "current_students_count",
            "is_available",
        )
        read_only_fields = ("created_at", "current_students_count", "is_available")

    def validate(self, attrs):
        image_url = attrs.pop("image_url", None)
        if image_url:
            import urllib.request
            from django.core.files.base import ContentFile
            import os
            response = urllib.request.urlopen(image_url)
            file_name = os.path.basename(image_url)
            attrs["image"] = ContentFile(response.read(), name=file_name)
        return attrs