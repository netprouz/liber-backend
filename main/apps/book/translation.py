from .models.book import Book
from modeltranslation.translator import TranslationOptions, translator


class BookTranslationOptions(TranslationOptions):
    fields = ('short_description', 'hard_cover')

translator.register(Book, BookTranslationOptions)