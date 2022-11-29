from django.core.validators import MinValueValidator
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
    inventory = models.IntegerField(validators=MinValueValidator(1))
    daily_fee = models.DecimalField(
        max_digits=3,
        decimal_places=2
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.title
