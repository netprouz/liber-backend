def count_book_view(book, user):
    from .models.view import View

    View.objects.get_or_create(book=book, owner=user)
