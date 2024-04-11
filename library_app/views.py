from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator

from .models import Book, Genre, Author

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

class BookListView(ListView):
    model = Book
    template_name = 'catalog/books.html'
    paginate_by = 10
    context_object_name = 'books'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instances = Book.objects.all()
        paginator = Paginator(instances, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['books_list'] = page_obj
        return context