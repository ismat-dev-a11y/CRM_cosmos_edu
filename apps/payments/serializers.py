from rest_framework import serializers
from .models import Payment


class PaymentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "user",
            "course",
            "amount",
            "provider",
            "note",
        ]

    def create(self, validated_data):
        request = self.context["request"]

        validated_data["created_by"] = request.user.userprofile
        validated_data["status"] = Payment.Status.PENDING

        return Payment.objects.create(**validated_data)


class PaymentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "user",
            "course",
            "amount",
            "provider",
            "note",
        ]

    def create(self, validated_data):
        validated_data["status"] = Payment.Status.PENDING
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


