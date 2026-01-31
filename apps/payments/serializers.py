from rest_framework import serializers
from .models import Payment
class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    course_name = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Payment
        fields = [
            'id',
            'user_name',
            'course',
            'course_name',
            'amount',
            'provider',
            'status',
            'transaction_id',
            'receipt_number',
            'payment_date',
            'note',
        ]
        read_only_fields = [
            'transaction_id',
            'receipt_number',
            'payment_date',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if 'amount' in representation and representation['amount'] is not None:
            representation['amount'] = float(representation['amount'])

        return representation