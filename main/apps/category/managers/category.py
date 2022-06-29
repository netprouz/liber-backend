from ...common.managers import BaseManager


class CategoryManager(BaseManager):
    def create_category_instance(self, owner, data):
        return self.create(owner=owner, **data)
