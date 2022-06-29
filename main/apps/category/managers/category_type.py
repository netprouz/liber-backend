from ...common.managers import BaseManager


class CategoryTypeManager(BaseManager):
    def create_category_type_instance(self, data):
        type__instances = []
        for type_ in data:
            type_[self.field.name] = self.instance
            type__instances.append(self.model(**type_))
        self.bulk_create(type__instances)
