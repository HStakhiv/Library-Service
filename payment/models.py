from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from borrowing.models import Borrowing
from user.models import User


class Payment(models.Model):
    PENDING = "PENDING"
    PAID = "PAID"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
    ]
    PAYMENT = "PAYMENT"
    FINE = "FINE"
    TYPE_CHOICES = [(PAYMENT, "Payment"), (FINE, "Fine")]
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    type = models.CharField(
        max_length=7, choices=TYPE_CHOICES, default=PAYMENT
    )
    borrowing_id = models.ForeignKey(
        to=Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    money_to_pay = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),
            MaxValueValidator(999.99),
        ],
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    # next fields will be added when session is implemented
    # session_url = models.URLField()
    # session_id = models.IntegerField(auto_created=True)
