from django.shortcuts import render
from django.views.generic import ListView
from .models import Book


# przy użyciu metody:
def home(request):
    content = {'all_books': Book.objects.all()}
    return render(request, 'wypozyczalnia/home.html', content)

# przy użyciu klasy:
# class BookListView:
#     model = 'book'
#     template = 'wypozyczalnia/home.html'
