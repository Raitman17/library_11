from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from library_app.models import Genre, Book, Author

OK = 200

class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_view_exists_by_url(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, OK)

    def test_view_exists_by_name(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, OK)

    def test_view_uses_template(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'catalog/books.html')





