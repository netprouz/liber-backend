from datetime import date

from ..account.models.user_book import BOOKSTATEChoices
from .models import Subscription

"""
 - check if there is an ending/expiring subscription
 - how is it measured?
    - if a subscription's end date is equal to today's date
    - it is disabled
 - remove all the books (that are temporary) from UserBook model

"""


# TODO: add cronjob for this function
def disable_active_subscriptions():
    today = date.today()
    subscriptions = Subscription.objects.filter(
        active=True,
        end_date=today,
    )
    if subscriptions.exists():
        for subscription in subscriptions:
            subscription.disable_instance()
            subscription.category.customer_books.filter(
                state=BOOKSTATEChoices.TEMPORARY,
            ).delete()
