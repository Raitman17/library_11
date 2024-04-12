from django.db import models
from uuid import uuid4
from datetime import datetime, timezone
from django.core.exceptions import ValidationError
from typing import Callable
from django.utils.translation import gettext_lazy as _
from django.conf.global_settings import AUTH_USER_MODEL

def get_datetime():
    return datetime.now(timezone.utc)

def check_created(dt: datetime) -> None:
    if dt > get_datetime():
        raise ValidationError(
            _('Datetime is bigger than current datetime!'),
            params={'created': dt}
        )
def check_modified(dt: datetime) -> None:
    if dt > get_datetime():
        raise ValidationError(
            _('Datetime is bigger than current datetime!'),
            params={'modified': dt}
        )

def validate_year(year: int) -> None:
    if year > get_datetime().year:
        raise ValidationError(
            _('Year is bigger than current year!'),
            params={'year': year},
        )

NAMES_MAX_LENGTH = 100
DESCRIPTION_MAX_LENGTH = 1000

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True

class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            check_created,
        ]
    )

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            check_modified,
        ]
    )

    class Meta:
        abstract = True

class Author(UUIDMixin, CreatedMixin, ModifiedMixin):
    full_name = models.TextField(_('full name'), null=False, blank=False, max_length=NAMES_MAX_LENGTH)

    books = models.ManyToManyField(
        'Book', through='BookAuthor',
        verbose_name=_('books'),
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = '"library"."author"'
        ordering = ['full_name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')

class Genre(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.TextField(_('name'), null=False, blank=False, max_length=NAMES_MAX_LENGTH)
    description = models.TextField(_('description'), null=True, blank=True, max_length=DESCRIPTION_MAX_LENGTH)

    books = models.ManyToManyField(
        'Book', through='BookGenre',
        verbose_name=_('books')
    )

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = '"library"."genre"'
        ordering = ['name']
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

book_types = (
    ('book', _('book')),
    ('magazine', _('magazine')),
)

class Book(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False, max_length=NAMES_MAX_LENGTH)
    description = models.TextField(_('description'), null=True, blank=True, max_length=DESCRIPTION_MAX_LENGTH)
    volume = models.PositiveIntegerField(_('volume'), null=False, blank=False)
    type = models.TextField(_('type'), null=True, blank=True, choices=book_types)
    year = models.IntegerField(_('year'), null=True, blank=True, validators=[validate_year])

    genres = models.ManyToManyField(
        Genre, through='BookGenre',
        verbose_name=_('genres'),
    )
    authors = models.ManyToManyField(
        Author, through='BookAuthor',
        verbose_name=_('authors'),
    )

    def __str__(self) -> str:
        return f'{self.title}, {self.type}, {self.volume} pages'

    class Meta:
        db_table = '"library"."book"'
        ordering = ['title', 'type', 'year']
        verbose_name = _('book')
        verbose_name_plural = _('books')

class BookGenre(UUIDMixin, CreatedMixin):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE,
        verbose_name=_('book'),
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        verbose_name=_('genre'),
    )

    def __str__(self) -> str:
        return f'{self.book} - {self.genre}'

    class Meta:
        db_table = '"library"."book_genre"'
        unique_together = (
            ('book', 'genre'),
        )
        verbose_name = _('Relationship book genre')
        verbose_name_plural = _('Relationships book genre')

class BookAuthor(UUIDMixin, CreatedMixin):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE,
        verbose_name=_('book'),
    )
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE,
        verbose_name=_('author'),
    )

    def __str__(self) -> str:
        return f'{self.book} - {self.author}'

    class Meta:
        db_table = '"library"."book_author"'
        unique_together = (
            ('book', 'author'),
        )
        verbose_name = _('Relationship book author')
        verbose_name_plural = _('Relationships book author')


# from django.conf.global_settings import AUTH_USER_MODEL
class Client(CreatedMixin, ModifiedMixin):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    money = models.DecimalField(
        verbose_name=_('money'),
        decimal_places=2,
        max_digits=10,
        default=0,
    )

    books = models.ManyToManyField(Book, through='BookClient', verbose_name=_('books'))

    def __str__(self) -> str:
        return f'{self.user.username} ({self.user.first_name} {self.user.last_name})'
    
    class Meta:
        db_table = '"library"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('clients')


class BookClient(UUIDMixin, CreatedMixin):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('book'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('client'))

    class Meta:
        db_table = '"library"."book_client"'
        unique_together = (
            ('book', 'client'),
        )
        verbose_name = _('relationship book client')
        verbose_name_plural = _('relationships book client')
