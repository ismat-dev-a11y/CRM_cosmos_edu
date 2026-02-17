from rest_framework import serializers
from .models import Enrollment, Attendance, Assignment


class EnrollmentSerializers(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source="student.full_name")
    course_title = serializers.ReadOnlyField(source="course.title")

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "student_name",
            "course",
            "course_title",
            "enrolled_at",
            "is_active",
            "is_paid",
        ]
        extra_kwargs = {"student": {"read_only": True}}

    def validate(self, attrs):
        student = attrs.get("student")
        course = attrs.get("course")

        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError(
                {"error": "Siz bu kursga allaqachon yozilgansiz!"}
            )
        if hasattr(course, "is_active") and not course.is_active:
            raise serializers.ValidationError({"course": "hozirda bu kurs yopilgan"})
        return attrs

    def validate_student(self, data):
        if data.role != "STUDENT":
            raise serializers.ValidationError("Faqat talabalar kursga yozila oladi")
        return data


class EnrollmenStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "enrolled_at", "is_active", "is_paid"]
        read_only_fields = ["student", "enrolled_at", "is_active", "is_paid"]


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"

    def create(self, validated_data):
        obj, created = Attendance.objects.update_or_create(
            lesson=validated_data["lesson"],
            student=validated_data["student"],
            defaults=validated_data
        )
        return obj

class AssignmentSerializer(serializers.ModelSerializer):
    lesson_title = serializers.ReadOnlyField(source="lesson.title")

    class Meta:
        model = Assignment
        fields = [
            "id",
            "lesson",
            "lesson_title",
            "title",
            "description",
            "due_date",
            "max_score",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate_due_data(self, value):
        from django.utils import timezone

        if value < timezone.now():
            raise serializers.ValidationError("Due data utmishda bulishi mumkin emas")
        return value

    def validate_max_score(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Maksimal ball 0 dan katta bo'lishi kerak"
            )
        if value > 1000:
            raise serializers.ValidationError(
                "Maksimal ball juda katta (1000 dan oshmasin)"
            )
        return value
