from django.db import models
from uuid import uuid4
from datetime import datetime, timezone
from django.core.exceptions import ValidationError
from typing import Callable

def get_datetime():
    return datetime.now(timezone.utc)

def validate_datetime(field_name: str) -> Callable:
    def validator(dt: datetime) -> None:
        if dt > get_datetime():
            raise ValidationError(
                'Datetime is bigger than current datetime!',
                params={field_name: dt}
            )
    return validator

def validate_year(year: int) -> None:
    if year > get_datetime().year:
        raise ValidationError(
            f'Year {year} is bigger than current year!',
            params={'year': year},
        )

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True

class CreatedMixin(models.Model):
    created = models.DateTimeField(
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            validate_datetime('created')
        ]
    )

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            validate_datetime('modified')
        ]
    )

    class Meta:
        abstract = True

class Author(UUIDMixin, CreatedMixin, ModifiedMixin):
    full_name = models.TextField(null=False, blank=False)

    books = models.ManyToManyField('Book', through='BookAuthor')

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = '"library"."author"'
        ordering = ['full_name']

class Genre(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = '"library"."genre"'
        ordering = ['name']

book_types = (
    ('book', 'book'),
    ('magazine', 'magazine'),
)

class Book(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    volume = models.PositiveIntegerField(null=False, blank=False)
    type = models.TextField(null=True, blank=True, choices=book_types)
    year = models.IntegerField(null=True, blank=True, validators=[validate_year])

    genres = models.ManyToManyField(Genre, through='BookGenre')
    authors = models.ManyToManyField(Author, through='BookAuthor')

    def __str__(self) -> str:
        return f'{self.title}, {self.type}, {self.volume} pages'

    class Meta:
        db_table = '"library"."book"'
        ordering = ['title']

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