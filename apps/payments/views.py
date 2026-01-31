from rest_framework import generics, permissions, viewsets

#local
from .models import Payment
from .serializers import PaymentSerializer
from apps.users.permissions import IsAdmin, CanBeStudent

class PaymentViewSet(viewsets.ModelViewSet):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer

  def get_permissions(self):
    if self.action in ['create', 'update', 'partial_update', 'destroy']:
      return [IsAdmin()]
    return [CanBeStudent()]

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Payment.objects.all()
    return Payment.objects.filter(user=user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)