import requests
from bs4 import BeautifulSoup
import json
import lxml
import os


# env
BOT_TOKEN = "5889653549:AAEihjuRUOSipiegopGSQ0A0icP6IUbawH4"
USER_ID = ""
URL = "http://127.0.0.1:8000"


def login():
    url = f"{URL}/api/user/token/"
    json1 = {
    "Content-type": "text/javascript"
    }
    data = {
        "email": "test@test.test",
        "password": "test1234"
}
    response = requests.post(url=url, json=json1, data=data)
    soup = BeautifulSoup(response.text, "lxml")
    token = json.loads(soup.text)["access"]
    return token


def check_all_borrowing():
        headers = {
            "Authorize": f"Bearer {login()}",
        }
        session = requests.Session()
        url = f"{URL}/api/borrowings/"
        response = session.get(url=url, headers=headers).json()
        borrwings = []
        for borrowing in response:
            borrwings[borrowing.id] = borrowing

        with open(f"all_borrowings.json", "w") as file:
            json.dump(borrwings, file, indent=4, ensure_ascii=False)

check_all_borrowing()


def check_new_update():
    with open(f"all_borrowings.json") as file:
        old_borrwings = json.load(file)

    headers = {
        "Authorize": f"Bearer {login()}",
    }
    session = requests.Session()
    url = f"{URL}/api/borrowings/"
    response = session.get(url=url, headers=headers).json()
    new_borrowins = []
    for borrowing in response:
        borrowings_id = borrowing["id"]
        if borrowings_id in old_borrwings:
            continue
        else:
            print(borrowings_id)

# check_new_update()

    #         ad_link = item["share_url"]
    #         ad_body = item["body"]
    #         if "price" not in item:
    #             ad_price = None
    #         else:
    #             ad_price = str(item["price"]["value"]) + " " + item["price"]["suffix"]
    #         anno_dict[ad_id] = {
    #             "link": ad_link,
    #             "body": ad_body,
    #             "price": ad_price
    #         }
    #
    #         new_anno_dict[ad_id] = {
    #             "link": ad_link,
    #             "body": ad_body,
    #             "price": ad_price
    #         }
    #         with open(f"last_ann_dict_{sub_word}.json", "w") as file:
    #             json.dump(new_anno_dict, file, indent=4, ensure_ascii=False)
    #
    # with open(f"new_dict_{sub_word}.json", "w") as file:
    #     json.dump(anno_dict, file, indent=4, ensure_ascii=False)
    #
    #
    # return new_anno_dict

