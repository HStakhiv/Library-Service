import requests
from bs4 import BeautifulSoup
import json

#####TODO .env


def login():
    url = f"{URL}/api/user/token/"
    json1 = {"Content-type": "text/javascript"}
    data = {"email": EMAIL, "password": PASSWORD}
    response = requests.post(url=url, json=json1, data=data)
    soup = BeautifulSoup(response.text, "lxml")
    token = json.loads(soup.text)["access"]
    return token


HEADERS = {
    "Authorize": f"Bearer {login()}",
}


def check_all_borrowing():
    session = requests.Session()
    url = f"{URL}/api/borrowings/"
    response = session.get(url=url, headers=HEADERS).json()
    borrowings = {}
    for borrowing in response:
        borrowings[borrowing["id"]] = borrowing

    with open(f"all_borrowings.json", "w") as file:
        json.dump(borrowings, file, indent=4, ensure_ascii=False)
    return borrowings


def check_new_update():
    with open(f"all_borrowings.json") as file:
        old_borrowings = json.load(file)

    session = requests.Session()
    url = f"{URL}/api/borrowings/"
    response = session.get(url=url, headers=HEADERS).json()

    new_borrowings = {}

    for borrowing in response:
        borrowing_id = str(borrowing["id"])
        if borrowing_id in old_borrowings:
            continue
        else:
            new_borrowings[borrowing["id"]] = borrowing
            old_borrowings[borrowing["id"]] = borrowing

            with open(f"updated_borrowings.json", "w") as file:
                json.dump(new_borrowings, file, indent=4, ensure_ascii=False)

        with open(f"all_borrowings.json", "w") as file:
            json.dump(old_borrowings, file, indent=4, ensure_ascii=False)

    return new_borrowings


def check_unpaid_borrowing():
    session = requests.Session()
    url = f"{URL}/api/borrowings/?is_active=True"
    response = session.get(url=url, headers=HEADERS).json()
    unpaid_borrowings = {}
    for borrowing in response:
        unpaid_borrowings[borrowing["id"]] = borrowing

    return unpaid_borrowings
