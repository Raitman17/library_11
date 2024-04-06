from django.db import models
from uuid import uuid4
from datetime import datetime

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True

class CreatedMixin(models.Model):
    created = models.DateTimeField(null=True, blank=True, default=datetime.now)

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(null=True, blank=True, default=datetime.now)

    class Meta:
        abstract = True

class Author(UUIDMixin, CreatedMixin, ModifiedMixin):
    full_name = models.TextField(null=False, blank=False)

    books = models.ManyToManyField('Book', through='BookAuthor')

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = '"library"."author"'

class Genre(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = '"library"."genre"'

class Book(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    volume = models.PositiveIntegerField(null=False, blank=False)
    type = models.TextField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    genres = models.ManyToManyField(Genre, through='BookGenre')
    authors = models.ManyToManyField(Author, through='BookAuthor')

    def __str__(self) -> str:
        return f'{self.title}, {self.type}, {self.volume} pages'

    class Meta:
        db_table = '"library"."book"'

class BookGenre(UUIDMixin, CreatedMixin):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.book} - {self.genre}'

    class Meta:
        db_table = '"library"."book_genre"'
        unique_together = (
            ('book', 'genre'),
        )

class BookAuthor(UUIDMixin, CreatedMixin):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.book} - {self.author}'

    class Meta:
        db_table = '"library"."book_author"'
        unique_together = (
            ('book', 'author'),
        )