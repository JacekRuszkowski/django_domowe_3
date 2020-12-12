from django import forms
from .models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        Book.slug = Book.title
        fields = ['title', 'author', 'description', 'pages', 'image', 'copies', 'category', 'slug']



class SearchForm(forms.ModelForm):
    q = forms.CharField(label="Szukaj...", max_length=30)

