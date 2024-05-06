from django.test import TestCase
from typing import Iterable
from django.core.exceptions import ValidationError
from datetime import date, datetime, timezone, timedelta
from django.contrib.auth.models import User

from library_app.models import Book, Genre, Author, Client, check_created, check_modified, check_positive, validate_year

def create_model_test(model_class, valid_attrs: dict, bunch_of_invalid_attrs: Iterable = None):
    class ModelTest(TestCase):
        def test_unsuccessful_creation(self):
            if bunch_of_invalid_attrs:
                for invalid_attrs in bunch_of_invalid_attrs:
                    with self.assertRaises(ValidationError):
                        model_class.objects.create(**invalid_attrs)
        
        def test_successful_creation(self):
            model_class.objects.create(**valid_attrs)
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

class ClientTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc', first_name='abc', last_name='abc', password='abc')

    def test_invalid(self):
        with self.assertRaises(ValidationError):
            Client.objects.create(user=self.user, money=-1)

    def test_create_and_str(self):
        self.assertEqual(str(Client.objects.create(user=self.user)), 'abc (abc abc)')


def create_str_test(model_class, attrs, expected_str):
    def test(self):
        self.assertEqual(str(model_class.objects.create(**attrs)), expected_str)
    return test

str_test_data = (
    (Book, {'title': 'ABC', 'type': 'book', 'volume': 1}, 'ABC, book, 1 pages'),
    (Genre, {'name': 'ABC', 'description': 'ABC'}, 'ABC'),
    (Author, {'full_name': 'ABC'}, 'ABC'),
)

str_methods = {f'test_{args[0].__name__}': create_str_test(*args) for args in str_test_data}
StrTest  = type('StrTest', (TestCase,), str_methods)

PAST = datetime(datetime.today().year-1, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)
FUTURE = datetime(datetime.today().year+1, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)

validators_pass = (
    (check_positive, 1),
    (check_created, PAST),
    (check_modified, PAST),
    (validate_year, PAST.year),
)

validators_fail = (
    (check_positive, -1),
    (check_created, FUTURE),
    (check_modified, FUTURE),
    (validate_year, FUTURE.year),
)

def create_val_test(validator, value, valid=True):
    def test(self):
        with self.assertRaises(ValidationError):
            validator(value)
    return lambda _ : validator(value) if valid else test

invalid_methods = {f'test_inval_{args[0].__name__}': create_val_test(*args, valid=False) for args in validators_fail}
valid_methods = {f'test_val_{args[0].__name__}': create_val_test(*args) for args in validators_pass}

ValidatorsTest = type('ValidatorsTest', (TestCase,), invalid_methods | valid_methods)
