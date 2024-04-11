from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/', views.view_book, name='book'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/', views.view_author, name='author'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genre/', views.view_genre, name='genre'),
]