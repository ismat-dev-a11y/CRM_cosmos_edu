# core/serializers.py
from rest_framework import serializers
from .models import Certificate,CenterSettings

class CertificateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Certificate
        fields = ['id', 'title', 'image', 'received_date']

class CenterSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterSettings
        fields = [
            "center_name",
            "short_name",
            "phone",
            "email",
            "address",
            "working_hours"
        ]