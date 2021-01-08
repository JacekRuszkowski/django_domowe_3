from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category, OrderItem, Order
from .forms import BookForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q


# przy użyciu metody:
def home(request):
    categories = Category.objects.all()
    books = Book.objects.all()
    context = {'categories': categories,
               'books': books,
               }
    return render(request, 'wypozyczalnia/home.html', context)


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


def add_to_cart(request, slug):
    item = get_object_or_404(Book, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    # order query set
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0] # był błąd przez to?
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item) # skąd się wzięło tutaj "items"? bo to jest słownik?
    messages.success(request, f'Książka dodana do koszyka???')
    return redirect("book-detail", slug=item.slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Book, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
