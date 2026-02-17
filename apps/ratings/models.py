from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import UserProfile
from apps.courses.models import Course
from apps.main.models import TimeStampedModel


class ActiveRatingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Rating(TimeStampedModel):
    student = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="given_ratings"
    )
    mentor = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="received_ratings"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")

    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveRatingManager()

    class Meta:
        unique_together = ("student", "mentor", "course")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} → {self.mentor} | {self.course} | {self.score}"
