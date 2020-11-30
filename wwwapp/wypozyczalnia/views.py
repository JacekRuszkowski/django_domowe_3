from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category
from .forms import BookForm
from django.contrib import messages
from django.views.generic import CreateView, DetailView


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
    categories = Category.objects.all()
    books = Book.objects.all()
    content = {'category': category,
               'books': books,
               'categories': categories,
               }
    return render(request, 'wypozyczalnia/category_view.html', content)

def books_by_author(request, author):
    categories = Category.objects.all()
    books = Book.objects.filter(author=author)
    content = {
        'books': books,
        'categories': categories,
    }
    return render(request, 'wypozyczalnia/author.html', content)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    categories = Category.objects.all()
    content = {'book': book,
               'categories': categories}
    return render(request, 'wypozyczalnia/book_detail.html', content)


def book_add(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Dodano nową książkę')
        return redirect('book-detail', slug=book.slug)
    else:
        form = BookForm()
    content = {'form': form, 'categories': categories}
    return render(request, 'wypozyczalnia/book_edit.html', content)


def book_edit(request, slug):
    book = get_object_or_404(Book, slug=slug)
    categories = Category.objects.all()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Zmiany zapisane')
            return redirect('book-detail', slug=book.slug)
    else:
        form = BookForm(instance=book)
    content = {'form': form, 'categories': categories}
    return render(request, 'wypozyczalnia/book_edit.html', content)


def book_delete(request, slug):
    book = get_object_or_404(Book, slug=slug)
    categories = Category.objects.all()
    if request.method == "POST":
        book.delete()
        messages.success(request, f'Książka usunięta')
        return redirect('home')
    content = {'book': book,
               'categories': categories}
    return render(request, 'wypozyczalnia/book_delete.html', content)
