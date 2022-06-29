from ...common.managers import BaseManager


class RateManager(BaseManager):
    def create_rate_instance(self, owner, data):
        instance = self.create(**data, owner=owner)
        return instance
