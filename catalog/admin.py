from django.contrib import admin

from catalog.models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "pages", "is_available", "published_at")
    list_filter = ("category", "is_available")
    search_fields = ("title", "author")