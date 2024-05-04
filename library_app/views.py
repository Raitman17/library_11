from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core import paginator as django_paginator, exceptions
from rest_framework import viewsets, permissions, authentication
from django.contrib.auth import decorators, mixins

from .serializers import BookSerializer, AuthorSerializer, GenreSerializer
from .models import Book, Genre, Author, Client
from .forms import RegistrationForm, AddFundsForm

def home_page(request):
    return render(
        request,
        'index.html',
        {
            'books': Book.objects.count(),
            'authors': Author.objects.count(),
            'genres': Genre.objects.count(),
        }
    )

def create_listview(model_class, plural_name, template):
    class CustomListView(mixins.LoginRequiredMixin, ListView):
        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            instances = model_class.objects.all()
            paginator = django_paginator.Paginator(instances, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return CustomListView

def create_view(model_class, context_name, template, redirect_page):
    @decorators.login_required
    def view(request):
        id_ = request.GET.get('id', None)
        if not id_:
            return redirect(redirect_page)
        try:
            target = model_class.objects.get(id=id_) if id_ else None
        except exceptions.ValidationError:
            return redirect(redirect_page)
        if not target:
            return redirect(redirect_page)
        context = {context_name: target}
        if model_class == Book:
            client = Client.objects.get(user=request.user)
            context['client_has_book'] = target in client.books.all()
        return render(
            request,
            template,
            context,
        )
    return view

view_book = create_view(Book, 'book', 'entities/book.html', 'books')
view_author = create_view(Author, 'author', 'entities/author.html', 'authors')
view_genre = create_view(Genre, 'genre', 'entities/genre.html', 'genres')

BookListView = create_listview(Book, 'books', 'catalog/books.html')
AuthorListView = create_listview(Author, 'authors', 'catalog/authors.html')
GenreListView = create_listview(Genre, 'genres', 'catalog/genres.html')

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return redirect('homepage')
    else:
        form = RegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'form': form},
    )

class MyPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ('POST', 'DELETE', 'PUT'):
            return bool(request.user and request.user.is_superuser)
        return False

def create_viewset(model_class, serializer):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [MyPermission]

    return ViewSet

BookViewSet = create_viewset(Book, BookSerializer)
AuthorViewSet = create_viewset(Author, AuthorSerializer)
GenreViewSet = create_viewset(Genre, GenreSerializer)

@decorators.login_required
def profile(request):
    form_errors = ''
    client = Client.objects.get(user=request.user)
    if request.method == 'POST':
        form = AddFundsForm(request.POST)
        if form.is_valid():
            money = form.cleaned_data.get('money')
            client.money += money
            client.save()
    else:
        form = AddFundsForm()

    return render(
        request,
        'pages/profile.html',
        {
            'form': form,
            'form_errors': form_errors,
            'client_data': {'username': client.user.username, 'money': client.money},
            'client_books': client.books.all(),
        }
    )

@decorators.login_required
def buy(request):
    book_id = request.GET.get('id', None)
    if not book_id:
        return redirect('books')
    try:
        book = Book.objects.get(id=book_id) if book_id else None
    except exceptions.ValidationError:
        return redirect('books')
    if not book:
        return redirect('books')
    
    client = Client.objects.get(user=request.user)

    if request.method == 'POST' and client.money >= book.price and book not in client.books.all():
            client.books.add(book)
            client.money -= book.price
            client.save()

    return render(
        request,
        'pages/buy.html',
        {
            'client_has_book': book in client.books.all(),
            'money': client.money,
            'book': book,
        }
    )
