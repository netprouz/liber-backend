from ...common.managers import BaseManager


class BalanceManager(BaseManager):
    def create_balance_instance(self, owner, data):
        return self.create(owner=owner, **data)
