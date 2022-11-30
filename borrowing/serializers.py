from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    # is_active = serializers.BooleanField(source="borrowing.is_active", read_only=True)
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            # "is_active",
            # "user",
        )
        # write_only_fields = ["is_active", ]


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=True, read_only=True)


class BorrowingAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            # "is_active",
            "user",
        )


class BorrowingAdminDetailSerializer(BorrowingAdminSerializer):
    book = BookSerializer(many=True, read_only=True)
