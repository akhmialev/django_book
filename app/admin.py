from django.contrib import admin
from .models import Category, Book, Author


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_authors_list', 'get_category_list']

    def get_authors_list(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])

    get_authors_list.short_description = 'Authors'

    def get_category_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_authors_list.short_description = 'Category'


admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(Author)
