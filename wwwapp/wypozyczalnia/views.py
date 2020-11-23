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


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    categories = Category.objects.all()
    content = {'book': book,
               'categories': categories}
    return render(request, 'wypozyczalnia/book_detail.html', content)


def book_add(request):
    categories = Category.objects.all()
    if request.method == "POST":
        messages.success(request, 'Dodano nową książkę')
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
        return redirect('book-detail', slug=book.slug)
    else:
        form = BookForm()
    content = {'form': form, 'categories': categories}
    return render(request, 'wypozyczalnia/book_edit.html', content)


def book_edit(request, slug):
    book = get_object_or_404(Book, slug=slug)
    categories = Category.objects.all()
    if request.method == "POST":  # tutaj coś nie działa. Nie widzi POST?
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # book = book.save()
            book.save()
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
        return redirect('home')
    content = {'book': book,
               'categories': categories}
    return render(request, 'wypozyczalnia/book_delete.html', content)
