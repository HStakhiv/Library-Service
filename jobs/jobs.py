# from django.conf import settings
# import json
from borrowing.models import Borrowing
from datetime import datetime, timedelta


def schedule_api():
    today = datetime.now()
    tomorrow = today + timedelta(1)
    queryset = Borrowing.objects.filter(expected_return_date=tomorrow)
    print(f"You have {queryset} book to return")

