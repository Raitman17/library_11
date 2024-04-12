from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/', views.view_book, name='book'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/', views.view_author, name='author'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genre/', views.view_genre, name='genre'),
    path('test_form/', views.form_test_page, name='test_form'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]