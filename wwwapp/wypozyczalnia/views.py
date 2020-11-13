from django.shortcuts import render
from .models import Book, Category


# przy użyciu metody:
def home(request):
    categories = Category.objects.all()
    books = Book.objects.all()
    content = {'categories': categories,
               'books': books,
               }
    return render(request, 'wypozyczalnia/home.html', content)


def category(request, slug):
    category = Category.objects.get(slug=slug)
    books = Book.objects.all()
    content = {'category': category,
               'books': books,
               }
    return render(request, 'wypozyczalnia/category_view.html', content)
