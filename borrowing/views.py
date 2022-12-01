from datetime import datetime, timedelta

from rest_framework import viewsets
# from rest_framework.permissions import IsAdminUser

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer, BorrowingCreateSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    # permission_classes = (IsAuthenticated,)
    #
    # def get_queryset(self):
    #     return Borrowing.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailyViewSet(viewsets.ModelViewSet):
    today = datetime.now()
    tomorrow = today + timedelta(1)
    queryset = Borrowing.objects.filter(expected_return_date=tomorrow)
    serializer_class = BorrowingSerializer
    # permission_classes = (IsAdminUser,)
