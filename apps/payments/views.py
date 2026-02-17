from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Payment
from .serializers import (
    PaymentCreateSerializer,
    # PaymentReadSerializer,
)
from apps.users.permissions import IsAdmin


@extend_schema_view(
    list=extend_schema(tags=["Payments"]),
    retrieve=extend_schema(tags=["Payments"]),
    create=extend_schema(tags=["Payments"]),
    update=extend_schema(tags=["Payments"]),
    partial_update=extend_schema(tags=["Payments"]),
    destroy=extend_schema(tags=["Payments"]),
)
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]