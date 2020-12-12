from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category
from .forms import BookForm
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q


# przy użyciu metody:
def home(request):
    categories = Category.objects.all()
    books = Book.objects.all()
    content = {'categories': categories,
               'books': books,
               }
    return render(request, 'wypozyczalnia/home.html', content)


def search_results(request):
    categories = Category.objects.all()
    query = request.GET.get('q')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    )
    context = {
        'categories': categories,
        'books': books
    }
    return render(request, 'wypozyczalnia/search_results.html', context)


### w ten sposób można zrobic za pomoca generic views, ale nie wiem jak wrzucić tam kategorie.
# class SearchResultsView(ListView):
#     model = Book
#     template_name = 'wypozyczalnia/search_results.html'
#     context_object_name = 'books'
#
#     def get_queryset(self):
#         category = Category.objects.all()
#         context = {
#             'category':category
#         }
#         query = self.request.GET.get('q')
#         books = Book.objects.filter(
#             Q(title__icontains=query) | Q(author__icontains=query)
#         )
#         return books, context


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
    author_name = author
    content = {
        'books': books,
        'categories': categories,
        'author_name': author_name,
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


# funkcja, któtra zamienia slug dodawanej książki jeśli jest to dokładnie ta sama książka.
# dodaje do pola slug numer id ksiazki zmieniony na str.
# >>> for book in books:
# ...     if book.slug == 'dorota':
# ...             new_id == str(book.id)
# ...             book.slug += new_id
# ...             book.save()
# ...
# >>> for book in books:
# ...     book.slug




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



