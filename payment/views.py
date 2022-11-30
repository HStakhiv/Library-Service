from rest_framework import viewsets

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentAdminListSerializer
)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.prefetch_related("borrowing_id")
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action == "list" and self.request.user.is_staff:
            return PaymentAdminListSerializer

        return PaymentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
