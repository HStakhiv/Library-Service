from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from payment.models import Payment
from payment.serializers import PaymentSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
        read_only_fields = [
            "actual_return_date",
        ]


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
            borrowing_data = Borrowing.objects.create(**validated_data)
            Payment.objects.create(
                status="PENDING",
                money_to_pay=borrowing_data.book.daily_fee,
                borrowing_id=borrowing_data,
                user_id=borrowing_data.user_id,
            )
            Borrowing.decrease_book_inventory(pk=borrowing_data.book.id)
            borrowing_data.save()
            return borrowing_data


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


class BookReturnBorrowingSerializer(BorrowingSerializer):
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
        read_only_fields = (
            "user",
            "borrow_date",
            "expected_return_date",
            "book",
        )

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        if self.instance.actual_return_date:
            raise ValidationError("You already borrow this book")
        return data

    def create(self, validated_data):
        return Borrowing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.actual_return_date = instance.set_actual_data()
            Borrowing.increase_book_inventory(pk=instance.book.id)
            instance.save()
            return instance
