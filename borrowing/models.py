from datetime import datetime

from django.conf import settings
from django.db import models

from book.models import Book
from user.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        Book, related_name="borrowing_books", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="borrowing_user",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["borrow_date"]

    @staticmethod
    def decrease_book_inventory(pk):
        book = Book.objects.get(pk=pk)
        book.inventory -= 1
        book.save()

    @staticmethod
    def increase_book_inventory(pk):
        book = Book.objects.get(pk=pk)
        book.inventory += 1
        book.save()

    @staticmethod
    def set_actual_data():
        return str(datetime.now()).split()[0]
