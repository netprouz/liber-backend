from .models import Transaction
from ..account.models.balance import Balance


def initialize_transaction(owner, price, transaction_type):
    obj = Transaction.objects.create(
        owner=owner,
        total_price=price,
        transaction_type=transaction_type,
    )
    return obj.id


def pay_transaction(transaction_id):
    try:
        instance = Transaction.objects.get(id=transaction_id)
        instance.make_payment()
        create_user_balance(instance.owner, instance.total_price)
    except Transaction.DoesNotExist:
        return


def cancel_transaction(transaction_id):
    try:
        instance = Transaction.objects.get(id=transaction_id)
        instance.cancel()
    except Transaction.DoesNotExist:
        return


def create_user_balance(owner, amount):
    Balance.objects.create(owner=owner, amount=amount)
