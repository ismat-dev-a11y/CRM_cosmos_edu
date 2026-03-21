from django.db import models
from django.conf import settings
from apps.groups.models import Group
from apps.users.models import UserProfile
from apps.storedfiles.models import StoredFile


class HomeworkTask(models.Model):
    # homework_tasks: group_id, title, deadline_at, created_by
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="homework_tasks")
    title = models.CharField(max_length=255)
    deadline_at = models.DateTimeField(blank=True, null=True)
    file_url = models.URLField(max_length=500)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_homework_tasks",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group} - {self.title}"


class HomeworkSubmission(models.Model):
    # homework_submissions: homework_task_id, student_id, status, submitted_at
    class Status(models.TextChoices):
        NOT_SUBMITTED = "not_submitted", "Not submitted"
        SUBMITTED = "submitted", "Submitted"
        DONE = "done", "Done"
        NEEDS_REVISION = "needs_revision", "Needs revision"

    homework_task = models.ForeignKey(HomeworkTask, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="homework_submissions")
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.SUBMITTED)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # ERD da file ko‘rsatilmagan, lekin amalda kerak bo‘ladi.
    file_url = models.URLField(max_length=500)

    class Meta:
        unique_together = ("homework_task", "student")

    def __str__(self):
        return f"{self.student} -> {self.homework_task}"