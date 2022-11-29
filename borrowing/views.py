from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
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

        return BorrowingSerializer
