from ...common.managers import BaseManager


class BookTypeManager(BaseManager):
    def create_book_type(self, book_types):
        book_content_instances = []
        for book_type in book_types:
            book_type[self.field.name] = self.instance
            book_content_instances.append(self.model(**book_type))
        self.bulk_create(book_content_instances)
