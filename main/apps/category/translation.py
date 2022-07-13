from .models import Category
from modeltranslation.translator import TranslationOptions, translator



class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(Category, CategoryTranslationOptions)