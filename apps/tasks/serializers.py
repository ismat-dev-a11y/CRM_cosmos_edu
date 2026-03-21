from rest_framework import serializers
from apps.tasks.models import HomeworkTask, HomeworkSubmission


class HomeworkTaskSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source="group.name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = HomeworkTask
        fields = ["id", "group", "group_name", "title", "deadline_at", "created_by", "created_by_name", "created_at", 'file_url']
        read_only_fields = ["id", "created_by", "created_at"]


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    task_title = serializers.CharField(source="homework_task.title", read_only=True)
    # file_url = serializers.CharField(source="file.url", read_only=True)

    class Meta:
        model = HomeworkSubmission
        fields = [
            "id",
            "homework_task", "task_title",
            "student", "student_name",
            "status", "submitted_at",
            "file_url",
        ]
        read_only_fields = ["id", "submitted_at"]