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
    image = serializers.ImageField()
    class Meta:
        model = Course
        fields = (
            "image",
            "current_students_count",
            "is_available",
            "created_at",
        )
