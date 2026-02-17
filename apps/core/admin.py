from django.contrib import admin
from .models import Certificate, CenterSettings
from unfold.admin import ModelAdmin


@admin.register(Certificate)
class CertificateAdmin(ModelAdmin):
    list_display = ("title", "image", "received_date")
    list_filter = ("received_date",)


@admin.register(CenterSettings)
class CenterSettingsAdmin(ModelAdmin):
    list_display = ["center_name", "phone", "email"]
