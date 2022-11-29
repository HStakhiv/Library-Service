from django.test import TestCase

from book.models import Book


class ModelsTest(TestCase):
    def test_book_format_str(self):
        book = Book.objects.create(
            title="testname",
            author="test",
            daily_fee=6.99,
        )
        self.assertEqual(
            str(book), f"{book.title}-{book.author}: {book.daily_fee}$/day"
        )
