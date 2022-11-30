from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# from book.models import Book
from book.serializers import BookSerializer
from borrowing.models import Borrowing


# class BookBorrowingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = "__all__"
#
#     def validate(self, attrs):
#         data = super(BookBorrowingSerializer, self).validate(attrs)
#         Book.validate_inventory(attrs["inventory"], ValueError)
#         return data


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
        )
        read_only_fields = ["actual_return_date", ]


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)


class BorrowingCreateSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
        read_only_fields = ["actual_return_date"]

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        inventory = data["book"]
        if inventory.inventory < 1:
            raise ValidationError("You can't borrow this book")

        return data

    def create(self, validated_data):
        with transaction.atomic():
            books_data = Borrowing.objects.create(**validated_data)
            Borrowing.decrease_book_inventory(pk=books_data.book.id)
            books_data.save()
            return books_data


class BorrowingAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingAdminDetailSerializer(BorrowingAdminSerializer):
    book = BookSerializer(many=False, read_only=True)
