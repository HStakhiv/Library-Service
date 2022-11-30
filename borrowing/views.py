from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer, BorrowingAdminSerializer, BorrowingAdminDetailSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            if self.request.user.is_staff:
                return BorrowingAdminSerializer
            return BorrowingSerializer

        if self.action == "retrieve":
            if self.request.user.is_staff:
                return BorrowingAdminDetailSerializer
            return BorrowingDetailSerializer



        return BorrowingSerializer

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")

        queryset = self.queryset

        if is_active:
            queryset = self.queryset.filter(actual_return_date__isnull=eval(is_active))
            # x = [obj.id for obj in queryset if obj.is_active is eval(is_active)]
            # queryset = self.queryset.filter(id__in=x)

        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
