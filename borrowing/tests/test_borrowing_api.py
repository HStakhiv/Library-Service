from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from book.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer

BORROWING_URL = "http://127.0.0.1:8000/api/borrowings/"


class UnauthenticatedBorrowingApiViewTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiViewTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )

        self.client.force_authenticate(self.user)

    def sample_book(self, **params):
        defaults = {
            "title": "Sample movie",
            "author": "test",
            "cover": "testname",
            "inventory": 1,
            "daily_fee": 7.99,
        }
        defaults.update(params)

        return Book.objects.create(**defaults)

    def sample_borrowing(self, **params):
        defaults = {
            "expected_return_date": "2020-08-08",
            "book": self.sample_book(),
            "user": self.user
        }
        defaults.update(params)

        return Borrowing.objects.create(**defaults)

    def test_list_borrowing(self):
        self.sample_borrowing()
        self.sample_borrowing()

        res = self.client.get(BORROWING_URL)

        borrowings = Borrowing.objects.all()
        serializer = BorrowingSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowing_filter(self):
        borrowing = self.sample_borrowing()

        response = self.client.get(BORROWING_URL, {"is_active": True})
        serializer = BorrowingSerializer(borrowing)

        self.assertIn(serializer.data, response.data)

    def test_creat_borrowing_bad_request(self):
        payload = {
            "expected_return_date": "2021-07-07",
        }

        response = self.client.post(BORROWING_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
