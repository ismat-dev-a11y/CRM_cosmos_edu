# core/serializers.py
from rest_framework import serializers
from .models import Certificate, CenterSettings


class CertificateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Certificate
        fields = ["id", "title", "image", "received_date"]



class CenterSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CenterSettings
        fields = "__all__"
        read_only_fields = ["id", "updated_at"]



