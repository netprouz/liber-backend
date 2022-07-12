from ..common.managers import BaseManager
from .utils import generate_random_string


class OrderManager(BaseManager):
    def create_order_instance(self, user, data):
        from ..account.models.user_book import BOOKSTATEChoices, UserBook
        from ..book.models.book_type import TYPEChoices
        from .models import PAYMENTTypeChoices

        is_paid = False
        is_completed = False
        price = data.get("book_type").price
        payment_type = data.get("payment_type")
        quantity = data.get("quantity", 1)

        # TODO: send PAYMe to subtract balance
        if data.get("book_type").book_type == TYPEChoices.PAPER:
            price *= quantity
        if payment_type == PAYMENTTypeChoices.ONLINE:
            is_paid = True
            is_completed = True
            user.create_balance(-price)

        """
        The given book should be added to user book list
        """
        if (data.get("book_type").book_type == TYPEChoices.ONLINE) or (
            data.get("book_type").book_type == TYPEChoices.AUDIO
        ):
            UserBook.objects.get_or_create(
                category=data.get("book").category,
                owner=user,
                book=data.get("book"),
                state=BOOKSTATEChoices.PERMANENT,
                book_type=data.get("book_type").book_type,
            )

        return self.create(
            owner=user,
            total_price=price,
            is_paid=is_paid,
            is_completed=is_completed,
            order_number=generate_random_string(),
            **data
        )
