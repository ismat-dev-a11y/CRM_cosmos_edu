from django.db import models
from apps.courses.models import Course


class Certificate(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="certificates/")  # FileField
    received_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"
        ordering = ["-received_date"]

class CenterSettings(models.Model):
    center_name = models.CharField(max_length=200, verbose_name="Markaz nomi")
    short_name = models.CharField(
        max_length=100,
        verbose_name="Qisqa nomi",
        blank=True
    )
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Manzil")
    working_hours = models.CharField(max_length=200, verbose_name="Ish vaqti")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Markaz sozlamalari"
        verbose_name_plural = "Markaz sozlamalari"

    def __str__(self):
        return self.center_name or "Center Settings"

    # ✅ Singleton getter
    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    # ✅ Singleton enforce
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


