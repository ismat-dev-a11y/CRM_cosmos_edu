from rest_framework import serializers
from .models import Room, GroupStudent, Group
from drf_spectacular.utils import extend_schema_field
from apps.users.models import UserProfile
class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["name", "capacity"]

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class GroupStudentSerializers(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    group_name = serializers.CharField(source="group.name", read_only=True)
    status = serializers.ChoiceField(choices=GroupStudent.StudentStatus.choices)

    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.filter(role="STUDENT"),
    )

    class Meta:
        model = GroupStudent
        fields = [
            "id",
            "group",
            "group_name",
            "student",
            "student_name",
            "status",
            "joined_at",
        ]
        read_only_fields = ["joined_at", "group_name", "student_name"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # GET da ID lar o'rniga nomlar
        rep["group"] = instance.group.name
        rep["student"] = instance.student.get_full_name()
        return rep

    def validate(self, data):
        group = data.get("group")
        student = data.get("student")

        # ✅ Update da o'zini exclude qiladi
        qs = GroupStudent.objects.filter(group=group, student=student)

        if self.instance:  # PUT/PATCH
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                {"error": "Bu talaba allaqachon shu guruhda mavjud."}
            )
        return data


class GroupSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.title", read_only=True)
    mentor_name = serializers.CharField(source="mentor.get_full_name", read_only=True)
    room_name = serializers.CharField(source="room.name", read_only=True)
    student_count = serializers.SerializerMethodField()  # ✅ to'g'irlandi (source="student.count" xato edi)

    # ✅ Swagger'da choices ko'rsatadi
    lesson_days = serializers.ChoiceField(choices=Group.LessonDays.choices)
    status = serializers.ChoiceField(choices=Group.GroupStatus.choices, required=False)

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "course",
            "course_name",
            "mentor",
            "mentor_name",
            "room",
            "room_name",
            "lesson_days",
            "start_time",
            "end_time",
            "start_date",
            "status",
            "max_students",
            "student_count",
        ]

    @extend_schema_field(serializers.IntegerField())
    def get_student_count(self, obj):
        return obj.students.count()

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                {"time_error": "Dars tugash vaqti boshlanishidan keyin bo'lishi shart."}
            )
        return data