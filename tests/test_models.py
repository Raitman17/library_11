from django.test import TestCase
from library_app.models import Book, Genre, Author

def create_model_test(model_class, attrs):
    class ModelTest(TestCase):
        def test_successful_creation(self):
            model_class.objects.create(**attrs)

    return ModelTest

book_attrs = {'title': 'A', 'type': 'book', 'volume': 100}

BookModelTest = create_model_test(Book, book_attrs)
AuthorModelTest = create_model_test(Author, {'full_name': 'ABC'})
GenreModelTest = create_model_test(Genre, {'name': 'ABC'})
