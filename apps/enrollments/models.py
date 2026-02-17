from django.db import models
from apps.users.models import UserProfile
from apps.courses.models import Course, Lesson


class Enrollment(models.Model):
    """Studentning kursga yozilishi"""

    student = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="enrollments",
        limit_choices_to={"role": "STUDENT"},
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ["student", "course"]

    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}"


class Attendance(models.Model):
    """Davomat jadvali"""

    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("excused", "Excused"),
    ]

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="attendances"
    )

    student = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="attendances",
        limit_choices_to={"role": "STUDENT"},
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="present")

    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    # class Meta:
        # unique_together = ["lesson", "student"]

    def __str__(self):
        return f"{self.student.full_name} - {self.lesson} - {self.status}"


class Assignment(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="assignments"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
