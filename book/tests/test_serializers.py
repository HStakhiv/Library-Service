from django.test import TestCase

from book.models import Book
from book.serializers import BookSerializer


class TestSerializers(TestCase):
    def setUp(self) -> None:
        self.book_attributes = {
            "title": "test",
            "author": "testname",
            "cover": "test",
            "inventory": 3,
            "daily_fee": 7.99,
        }
        self.serializer_data = {
            "title": "testtitle",
            "author": "test",
            "cover": "testcover",
            "inventory": 2,
            "daily_fee": 9.85,
        }
        self.book = Book.objects.create(**self.book_attributes)
        self.serializer = BookSerializer(instance=self.book)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(data.keys(), set(
            ["id", "title", "author", "cover", "inventory", "daily_fee"]
        ))
