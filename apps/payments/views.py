from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from drf_spectacular.utils import extend_schema

from .models import Payment
from .serializers import (
    PaymentSerializer,
    PaymentStatusUpdateSerializer,
)
from apps.users.permissions import IsAdmin, IsAuthenticatedAndActive

@extend_schema(
    tags=["Payments"],
)
class PaymentCreateView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(
    tags=["Payments"],
    summary="Payment detail"
)
class PaymentDetailView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        user = self.request.user

        if user.role in ["ADMIN", "BOSS"]:
            return Payment.objects.all()

        return Payment.objects.filter(user=user)

@extend_schema(
    tags=["Payments"],
    summary="Update payment status (Admin)"
)
class PaymentStatusUpdateView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentStatusUpdateSerializer
    permission_classes = [IsAuthenticatedAndActive, IsAdmin]

@extend_schema(
    tags=["Payments"],
    summary="My payments"
)
class MyPaymentsView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        return Payment.objects.filter(
            user=self.request.user
        ).order_by("-created_at")



@extend_schema(
    tags=["Payments"],
    summary="Payments statistics"
)
class PaymentStatsView(APIView):
    permission_classes = [IsAuthenticatedAndActive, IsAdmin]

    def get(self, request):

        total_income = (
            Payment.objects.filter(status="SUCCESS")
            .aggregate(total=Sum("amount"))
        )

        return Response({
            "total_income": total_income["total"] or 0,
            "successful_payments":
                Payment.objects.filter(status="SUCCESS").count(),
            "pending_payments":
                Payment.objects.filter(status="PENDING").count(),
        })


