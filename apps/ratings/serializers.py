# serializers.py
from rest_framework import serializers
from .models import Rating


# serializers.py
from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    mentor_name = serializers.CharField(source="mentor.get_full_name", read_only=True)
    course_name = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Rating
        fields = [
            "id",
            "student",
            "student_name",
            "mentor",
            "mentor_name",
            "course",
            "course_name",
            "score",
            "comment",
            "is_active",
            "created_at",
        ]
        read_only_fields = ("mentor", "created_at", "is_active")  # ✅ mentor avtomatik

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Ball 1 dan 5 gacha bo'lishi kerak.")
        return value

    def validate(self, data):
        request = self.context.get("request")
        if request and not self.instance:
            if Rating.objects.filter(
                mentor=request.user,           # ✅ mentor
                student=data.get("student"),   # ✅ studentga
                course=data.get("course"),
            ).exists():
                raise serializers.ValidationError(
                    {"error": "Siz bu studentga bu kurs uchun allaqachon baho bergansiz."}
                )
        return data


class RatingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["score", "comment"]

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Ball 1 dan 5 gacha bo'lishi kerak.")
        return value

class TopStudentSerializer(serializers.Serializer):
    student__id = serializers.IntegerField()
    student__first_name = serializers.CharField()
    student__last_name = serializers.CharField()
    avg_score = serializers.FloatField()
    total_ratings = serializers.IntegerField()