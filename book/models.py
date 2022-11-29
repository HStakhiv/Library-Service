from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Book(models.Model):
    HARD = "HARD"
    SOFT = "SOFT"
    COVER_CHOICES = [
        (HARD, "Hard"),
        (SOFT, "Soft"),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4,
        choices=COVER_CHOICES,
        default=HARD,
    )
    inventory = models.IntegerField(unique=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(5000),
    ])
    daily_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),
            MaxValueValidator(999.99),
        ],
    )

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.title}-{self.author}: {self.daily_fee}$/day"
