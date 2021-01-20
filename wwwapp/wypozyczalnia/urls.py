"""wwwapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import (home,
                    category,
                    book_edit,
                    book_add,
                    book_delete,
                    book_detail,
                    books_by_author,
                    search_results,
                    add_to_cart,
                    remove_from_cart,
                    cart_view)

urlpatterns = [
    path('', home, name='home'),
    path('category/<str:slug>/', category, name='categories'),
    path('author/<str:author>/', books_by_author, name='authors-books'),
    path('add/', book_add, name='book-add'),
    path('search/', search_results, name='search-results'),
    path('cart/', cart_view, name='cart-view'),
    path('<str:slug>/edit/', book_edit, name='book-edit'),
    path('<str:slug>/', book_detail, name='book-detail'),
    path('<str:slug>/delete/', book_delete, name='book-delete'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
]
