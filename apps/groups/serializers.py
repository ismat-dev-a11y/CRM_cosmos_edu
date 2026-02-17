from rest_framework import serializers
from .models import Room, GroupStudent, Group


class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["name", "capacity"]

class GroupStudentSerializers(serializers.ModelSerializer):

    class Meta:
        model = GroupStudent
        fields = ["id", "group", "student", "status", "joined_at"]
        read_only_fields = ["id", "joined_at"]

    def validate(self, attrs):
        group = attrs.get("group") or self.instance.group

        if not self.instance:
            if group.students.count() >= group.max_students:
                raise serializers.ValidationError(
                    {"error": f"Bu yerda joy qolmadi (Max: {group.max_students})"}
                )

        return attrs



class GroupSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.title", read_only=True)
    mentor_name = serializers.CharField(source="mentor.get_full_name", read_only=True)
    room_name = serializers.CharField(source="room.name", read_only=True)
    student_count = serializers.IntegerField(source="student.count", read_only=True)

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

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                {"time_error": "Dars tugash vaqti boshlanishidan keyin bo'lishi shart."}
            )
        return data
