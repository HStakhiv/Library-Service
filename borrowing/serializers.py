from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "actual_return_date", "book")


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=True, read_only=True)
