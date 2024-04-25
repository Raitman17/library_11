from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Author, Genre, Book, BookAuthor, BookGenre, Client, BookClient
from datetime import date
from django.utils.translation import gettext_lazy as _

class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1

class BookGenreInline(admin.TabularInline):
    model = BookGenre
    extra = 1

class BookClientInline(admin.TabularInline):
    model = BookClient
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = (BookClientInline,)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author
    inlines = (BookAuthorInline,)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    model = Genre

DECADE = 10

class NewestBookFilter(admin.SimpleListFilter):
    title = _('recency')
    parameter_name = 'recency'
    _ten_yo = '10yo'
    _twenty_yo = '20yo'

    def lookups(self, *args) -> list[tuple[Any, str]]:
        return [
            (self._ten_yo, _('Created in the last 10 years')),
            (self._twenty_yo, _('Created in the last 20 years')),
        ]
    def queryset(self, _: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == self._ten_yo:
            return queryset.filter(year__gte=date.today().year - DECADE)
        elif self.value() == self._twenty_yo:
            return queryset.filter(year__gte=date.today().year - DECADE * 2)
        return queryset

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    model = Book
    inlines = (BookAuthorInline, BookGenreInline)
    list_filter = (
        'type',
        'genres',
        NewestBookFilter,
    )

@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    model = BookGenre

@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    model = BookAuthor