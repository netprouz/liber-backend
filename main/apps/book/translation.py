from main.apps.category.models import Category
from .models.book import Book
from modeltranslation.translator import TranslationOptions, translator


class BookTranslationOptions(TranslationOptions):
    fields = ('short_description',)

translator.register(Book, BookTranslationOptions)