from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "user_name",
            "course",
            "amount",
            "provider",
            "status",
            "transaction_id",
            "receipt_number",
            "payment_date",
            "note",
            "created_at",
        ]

        read_only_fields = (
            "transaction_id",
            "receipt_number",
            "payment_date",
            "status",
            "user",
        )

class PaymentStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ["status", "note"]
