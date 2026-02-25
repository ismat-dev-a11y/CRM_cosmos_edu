# core/serializers.py
from rest_framework import serializers
from .models import Certificate, CenterSettings


class CertificateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Certificate
        fields = ["id", "title", "image", "received_date"]
        read_fields_only = ['id']






class CenterSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterSettings
        fields = [
            'id',
            'center_name',
            'short_name',
            'phone',
            'email',
            'address',
            'working_hours',
            'updated_at',
        ]
        read_only_fields = ['id', 'updated_at']