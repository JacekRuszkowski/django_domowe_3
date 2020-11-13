from django.shortcuts import render
from .models import Book, Category
from django.views.generic import ListView



# przy użyciu metody:
def home(request):
    content = {'books': Book.objects.all()}
    return render(request, 'wypozyczalnia/home.html', content)


class CategoryList(ListView):
    model = Category
    template_name = 'wypozyczalnia/category_view.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return  context

# def categories(request):
#     content = {'categories': Category.objects.all(),
#                'all_books': Book.objects.all(),
#                }
#     return render(request, 'wypozyczalnia/category_view.html', content)