from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'authors', views.AuthorViewSet)

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/', views.view_book, name='book'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/', views.view_author, name='author'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genre/', views.view_genre, name='genre'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('profile/', views.profile, name='profile'),
    path('buy/', views.buy, name='buy'),
    path('read/', views.read, name='read'),
]