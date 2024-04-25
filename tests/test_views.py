from django.test import TestCase
from django.test.client import Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from library_app.models import Genre, Book, Author, Client
from rest_framework import status

def create_method_with_auth(url, page_name, template):
    def method(self):
        self.client = TestClient()
        user = User.objects.create(username='user', password='user')
        Client.objects.create(user=user)
        self.client.force_login(user=user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)

        response = self.client.get(reverse(page_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    return method

def create_method_no_auth(url):
    def method(self):
        self.client = TestClient()
        self.assertEqual(self.client.get(url).status_code, status.HTTP_302_FOUND)
    return method

pages = (
    ('/books/', 'books', 'catalog/books.html'),
    ('/authors/', 'authors', 'catalog/authors.html'),
    ('/genres/', 'genres', 'catalog/genres.html'),
    ('/profile/', 'profile', 'pages/profile.html'),
)
methods_with_auth = {f'test_{page[1]}': create_method_with_auth(*page) for page in pages}
TestWithAuth = type('TestWithAuth', (TestCase,), methods_with_auth)

methods_no_auth = {f'test_{url}': create_method_no_auth(url) for url, _, _ in pages}
TestNoAuth = type('TestNoAuth', (TestCase,), methods_no_auth)

instance_pages = (
    ('/book/', 'book', 'entities/book.html'),
    ('/author/', 'author', 'entities/author.html'),
    ('/genre/', 'genre', 'entities/genre.html'),
)