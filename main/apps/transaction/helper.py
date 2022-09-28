from paycomuz import Paycom
from .models import Transaction
from .service import pay_transaction, cancel_transaction


class CheckTransaction(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(id=account['order_id'])
            if transaction.price != amount / 100:
                return self.INVALID_AMOUNT
        except Transaction.DoesNotExist:
            return self.ORDER_NOT_FOND
        return self.ORDER_FOUND

    def successfully_payment(self, account, transaction, *args, **kwargs):
        pay_transaction(transaction.order_key)

    def cancel_payment(self, account, transaction, *args, **kwargs):
        cancel_transaction(transaction.order_key)
