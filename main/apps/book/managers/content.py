from ...common.managers import BaseManager


class ContentManager(BaseManager):
    def create_content_instance(self, owner, data):
        instance = self.create(**data, owner=owner)
        return instance

    def get_content_detail(self):
        return self.select_related("book")
