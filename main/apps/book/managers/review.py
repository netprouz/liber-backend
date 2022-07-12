from ...common.managers import BaseManager


class ReviewManager(BaseManager):
    def create_review_instance(self, owner, data):
        return self.create(**data, owner=owner)
