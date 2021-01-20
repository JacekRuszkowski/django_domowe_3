from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category, OrderItem, Order
from .forms import BookForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator


# Tutaj strasznie duże sie dzieje, jakos trzeba to uprościć
# do każdej funkcji musze przekazywać model Order, żeby wyświetlało sie zamówienie w koszyku?
# nie można zrobic jakiejś jednej funkcji, która będzie to wyświetlać na każdej stronie?
def home(request):
    categories = Category.objects.all()
    paginator = Paginator(Book.objects.all(), 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    books = page_obj # wyświetlanie książek z podziałem na strony
    context = {
        'categories': categories,
        'books': books,
    }
    return render(request, 'wypozyczalnia/home-page.html', context)


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


# funkcje administaratora
# warunek zamiast dekoratora user_passes_test
@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@login_required
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
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            messages.warning(request, f'Możesz wyporzyczyć tylko jeden egzeplarz danej ksiazki.')
            return redirect('book-detail', slug=item.slug)
        elif order.items.count() == 3:
            messages.warning(request, f"W koszyku masz już 3 książki. Nie możesz wypożyczyć więcej.")
            return redirect('book-detail', slug=item.slug)
        else:
            order.items.add(order_item)
            messages.info(request, f'Książka Wypożyczona.')
            return redirect('book-detail', slug=item.slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item) # skąd się wzięło tutaj "items"? bo to jest słownik?
        messages.info(request, f'Książka dodana do koszyka.')
        return redirect("book-detail", slug=item.slug)


# dlaczego w adminie te rzeczy cały czas są po usunięciu?
# czy nie powinien usuwać całego obiektu order_item?
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]  # był błąd przez to?
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, f'Książka usunięta z koszyka.')
            return redirect("cart-view")
        else:
            messages.warning(request, f'Nie ma takiej książki w koszyku.')
            return redirect("book-detail", slug=item.slug)
    else:
        messages.warning(request, f'Nie masz aktywnego zamówienia.')
        return redirect("book-detail", slug=item.slug)


@login_required
def cart_view(request):
    order = Order.objects.get(user=request.user)
    items = order.items.all()
    items_count = order.items.count()
    context = {
        'items': items,
        'items_count': items_count,
    }
    return render(request, 'wypozyczalnia/cart_test.html', context)





