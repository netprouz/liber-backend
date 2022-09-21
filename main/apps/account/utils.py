import json
import random
import string

import requests
from django.conf import settings as s


def create_user_book_instance(user, category):
    from ..book.models.book import Book
    from ..book.models.content import BOOKTYPEChoices
    from .models.user_book import BOOKSTATEChoices, UserBook

    books = Book.objects.filter(category=category)

    """
    The aim of this function is the following:
     - when user subscribes to a category
     - we filter books by that category
     - create access for that user for those category->book->contents
    """
    user_book_instances = []
    for book in books:
        if not UserBook.objects.filter(
            book=book,
            owner=user,
            book_type=BOOKTYPEChoices.AUDIO,
        ).exists():
            audio = dict(
                category=book.category,
                book=book,
                book_type=BOOKTYPEChoices.AUDIO,
                state=BOOKSTATEChoices.TEMPORARY,
                owner=user,
            )
            user_book_instances.append(UserBook(**audio))
        if not UserBook.objects.filter(
            book=book,
            owner=user,
            book_type=BOOKTYPEChoices.ONLINE,
        ).exists():
            online = dict(
                category=book.category,
                book=book,
                book_type=BOOKTYPEChoices.ONLINE,
                state=BOOKSTATEChoices.TEMPORARY,
                owner=user,
            )

            user_book_instances.append(UserBook(**online))
    UserBook.objects.bulk_create(user_book_instances)


def generate_random_password():
    _int = "".join(random.choice(string.digits) for _ in range(5))
    return _int


# def send_password_as_sms(phone_number, password):
#     url = s.SMS_DOMAIN + "?token=" + s.SMS_TOKEN
#     data = {
#         "message": {"recipients": [str(phone_number)]},
#         "priority": "default",
#         "sms": {"content": f"your password for zukko system is: {password}"},
#     }

#     requests.post(url, data=json.dumps(data), timeout=5)
