from django.db import models

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ManyToManyField(Book, related_name="borrowed_books")
    # user = models.ForeignKey(User, related_name="borrowed_user")

    class Meta:
        ordering = ["borrow_date"]
