from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingAdminSerializer,
    BorrowingAdminDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")

        if is_active:
            return self.queryset.filter(actual_return_date__isnull=eval(is_active))

        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)

        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            if self.request.user.is_staff:
                return BorrowingAdminSerializer
            return BorrowingSerializer

        if self.action == "retrieve":
            if self.request.user.is_staff:
                return BorrowingAdminDetailSerializer
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
