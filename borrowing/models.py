from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True)
    book = models.ManyToManyField(Book, related_name="borrowed_books")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowing_user"
    )

    class Meta:
        ordering = ["borrow_date"]
