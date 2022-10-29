from .models.book import Book
from modeltranslation.translator import TranslationOptions, translator


class BookTranslationOptions(TranslationOptions):
    fields = ('short_description', 'hardcover')

translator.register(Book, BookTranslationOptions)