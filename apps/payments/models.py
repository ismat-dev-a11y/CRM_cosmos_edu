import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.users.models import UserProfile
from apps.main.models import TimeStampedModel
from apps.courses.models import Course


class Payment(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    class Provider(models.TextChoices):
        PAYME = "PAYME", "Payme"
        CLICK = "CLICK", "Click"
        CASH = "CASH", "Cash"
        BANK = "BANK", "Bank transfer"

    user = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name="payments"
    )

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )

    provider = models.CharField(max_length=20, choices=Provider.choices)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    receipt_number = models.CharField(max_length=50, unique=True, blank=True, null=True)

    payment_date = models.DateTimeField(null=True, blank=True)

    note = models.TextField(blank=True)

    class Meta:
        # ordering = ['-created_at']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.user} | {self.amount} | {self.status}"

    def save(self, *args, **kwargs):
        if self.status == self.Status.SUCCESS and not self.payment_date:
            self.payment_date = timezone.now()

        if self.status == self.Status.SUCCESS and not self.receipt_number:
            self.receipt_number = f"REC-{timezone.now().strftime('%Y%m%d')}-{str(self.transaction_id)[:6].upper()}"

        super().save(*args, **kwargs)
