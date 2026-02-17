from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from apps.users.models import UserProfile
from apps.main.models import SoftDeleteModel
from apps.courses.models import Course


class Room(models.Model):
    """Dars xonalari uchun model"""

    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class GroupStudent(models.Model):
    """
    Guruh va Talaba o'rtasidagi bog'liqlik (Through model).
    Bu model bazada indexing uchun juda qulay va qo'shimcha ma'lumot saqlashga imkon beradi.
    """

    class StudentStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "O'qimoqda"
        LEFT = "LEFT", "Chiqib ketgan"
        FROZEN = "FROZEN", "Muzlatilgan"

    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=StudentStatus.choices, default=StudentStatus.ACTIVE
    )
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        # Bir talaba bir guruhga ikki marta qo'shilmasligi uchun
        unique_together = ("group", "student")
        db_table = "groups_student_relation"


class Group(SoftDeleteModel):
    class GroupStatus(models.TextChoices):
        WAITING = "WAITING", "Kutilmoqda"
        ACTIVE = "ACTIVE", "Faol"
        FINISHED = "FINISHED", "Tugallangan"

    class LessonDays(models.TextChoices):
        ODD = "ODD", "Toq kunlar (Dush-Chor-Jum)"
        EVEN = "EVEN", "Juft kunlar (Sesh-Pay-Shan)"
        DAILY = "DAILY", "Har kuni"

    # db_index=True qidiruvni tezlashtiradi
    name = models.CharField(max_length=150, db_index=True)

    # PROTECT kurs o'chirib yuborilsa guruhlar omon qolishini ta'minlaydi
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="groups")

    mentor = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, related_name="mentor_groups"
    )

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    # ManyToMany bog'liqlik oraliq model orqali
    students = models.ManyToManyField(
        UserProfile, through=GroupStudent, related_name="student_groups", blank=True
    )

    lesson_days = models.CharField(
        max_length=10, choices=LessonDays.choices, default=LessonDays.ODD
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=10, choices=GroupStatus.choices, default=GroupStatus.WAITING
    )

    max_students = models.PositiveIntegerField(
        default=12, validators=[MinValueValidator(5), MaxValueValidator(30)]
    )

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"

    def __str__(self):
        return f"{self.name} ({self.course.title})"
