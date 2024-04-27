from django.test import TestCase
from typing import Iterable
from django.core.exceptions import ValidationError
from datetime import date, datetime, timezone, timedelta

from library_app.models import Book, Genre, Author

def create_model_test(model_class, valid_attrs: dict, bunch_of_invalid_attrs: Iterable = None):
    class ModelTest(TestCase):
        def test_successful_creation(self):
            model_class.objects.create(**valid_attrs)

        def test_unsuccessful_creation(self):
            if bunch_of_invalid_attrs:
                for invalid_attrs in bunch_of_invalid_attrs:
                    with self.assertRaises(ValidationError):
                        model_class.objects.create(**invalid_attrs)
    return ModelTest

book_attrs = {'title': 'A', 'type': 'book', 'volume': 100}
future = datetime.now(timezone.utc) + timedelta(days=1)
book_invalid_attrs = (
    {'title': 'A', 'type': 'book', 'volume': -1},
    {'title': 'A', 'type': '???', 'volume': 100},
    {'title': 'A', 'type': 'book', 'year': date.today().year + 1},
    {'title': 'A', 'type': 'book', 'price': -1},
    {'title': 'A', 'type': 'book', 'created': future},
    {'title': 'A', 'type': 'book', 'modified': future},
)
BookModelTest = create_model_test(Book, book_attrs, book_invalid_attrs)
AuthorModelTest = create_model_test(Author, {'full_name': 'ABC'})
GenreModelTest = create_model_test(Genre, {'name': 'ABC'})
