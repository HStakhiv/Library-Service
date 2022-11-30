# from django.urls import reverse

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from book.models import Book
from book.serializers import BookSerializer

BOOK_URL = "http://127.0.0.1:8000/api/books/"  # TODO: make best practice URL


def sample_book(**params):
    defaults = {
        "title": "Sample movie",
        "author": "test",
        "cover": "testname",
        "inventory": 1,
        "daily_fee": 7.99,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class UnauthenticatedBookApiViewTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiViewTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_list_book(self):
        sample_book()
        sample_book()

        response = self.client.get(BOOK_URL)

        movies = Book.objects.all()
        serializer = BookSerializer(movies, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_filter(self):
        book = sample_book(title="test")
        res = self.client.get(BOOK_URL, {"title": "test"})
        serializer = BookSerializer(book)
        self.assertIn(serializer.data, res.data)
