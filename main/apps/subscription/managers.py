from datetime import date, timedelta

from ..common.managers import BaseManager


class SubscriptionManager(BaseManager):
    def create_subscription_instance(self, owner, data):
        from ..account.utils import create_user_book_instance

        category_type = data.get("category_type")
        owner.create_balance(-category_type.price)

        create_user_book_instance(
            owner,
            data.get("category"),
        )

        today = date.today()
        days = timedelta(days=category_type.days)
        end_date = today + days

        return self.create(
            **data,
            owner=owner,
            price=category_type.price,
            begin_date=today,
            end_date=end_date
        )
