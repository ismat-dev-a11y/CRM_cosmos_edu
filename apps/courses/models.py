from django.db import models
from apps.users.models import UserProfile
class Course(models.Model):
    COURSE_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    level = models.CharField(
        max_length=20,
        choices=COURSE_LEVEL_CHOICES,
        default='beginner'
    )

    description = models.TextField(blank=True)
    max_students = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    duration_weeks = models.PositiveIntegerField(default=12)

    image = models.ImageField(upload_to='courses/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def current_students_count(self):
        return self.enrollments.filter(is_active=True).count()

    @property
    def is_available(self):
        return self.current_students_count < self.max_students and self.is_active

class Lesson(models.Model):
    DAYS_CHOICES = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course_lessons'
    )

    mentor = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='mentor_lessons',
        limit_choices_to={'role': 'MENTOR'}
    )

    day = models.CharField(
        max_length=3,
        choices=DAYS_CHOICES
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    title = models.CharField(max_length=200, default="Lesson")

    week_number = models.PositiveIntegerField(default=1)

    lesson_type = models.CharField(
        max_length=20,
        choices=[
            ('theory', 'Theory'),
            ('practice', 'Practice'),
            ('project', 'Project'),
            ('exam', 'Exam'),
        ],
        default='theory'
    )

    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.title} - Week {self.week_number}: {self.title}"
