from django.db import models
from apps.courses.models import Course

class Certificate(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sertifikat nomi")
    image = models.ImageField(upload_to='certificates/', verbose_name="Rasm", default='certificates/wallhaven-qr27rq_uCDgbI4.jpg')
    received_date = models.DateField(verbose_name="Olingan sana")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"
        ordering = ['-received_date']


class CenterSettings(models.Model):
    center_name = models.CharField(max_length=200, verbose_name="Markaz nomi")
    short_name = models.CharField(max_length=100, verbose_name="Qisqa nomi", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Manzil")
    working_hours = models.CharField(max_length=200, verbose_name="Ish vaqti")

    class Meta:
        verbose_name = "Markaz sozlamalari"
        verbose_name_plural = "Markaz sozlamalari"

    def __str__(self):
        return self.center_name

    @classmethod
    def get_settings(cls):
        """Bitta obyekt bo‘lishi uchun – Singleton"""
        obj, created = cls.objects.get_or_create(id=1)
        return obj

    def save(self, *args, **kwargs):
        self.id = 1  # Har doim bitta obyekt bo‘lishi uchun
        super().save(*args, **kwargs)