from django.contrib import admin

from .models import Category, CategoryType


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "guid", "owner")
    list_display_links = ("title",)
    search_fields = ["title"]


admin.site.register(Category, CategoryAdmin)


class CategoryTypeAdmin(admin.ModelAdmin):
    list_display = ("guid", "category", "id")
    list_display_links = ("guid",)


admin.site.register(CategoryType, CategoryTypeAdmin)
