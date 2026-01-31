from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class UserProfile(AbstractUser):
    class Role(models.TextChoices):
        BOSS = 'BOSS', 'Boss (Super Admin)'
        ADMIN = 'ADMIN', 'Admin'
        MENTOR = 'MENTOR', 'Mentor'
        STUDENT = 'STUDENT', 'Student'
        PARENT = 'PARENT', 'Parent'

    username = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        limit_choices_to={'role': 'PARENT'}
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.phone_number} ({self.role}) - ({self.username})"

    @property
    def is_boss(self):
        return self.role == self.Role.BOSS

    @property
    def is_admin_user(self):
        return self.role in [self.Role.BOSS, self.Role.ADMIN]
