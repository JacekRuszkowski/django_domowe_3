from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from users.models import Profile


# kategoria
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        unique_together = ('slug', 'parent_category',)
        ordering = ('name',)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


# książka
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    pages = models.CharField(max_length=50)
    image = models.ImageField(default='default.jpg', upload_to='book_images')
    copies = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title


# logika wypożyczania:
class OrderItem(models.Model): # to jest konkretna jedna książka, którą użytkownik wypozycza?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Book, on_delete=models.CASCADE) # czy usunięcie książki z koszyka nie spowoduje usunięcie ksiązki z bazy dancyh?
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.item.author} - "{self.item.title}".'


class Order(models.Model): # to jest lista wszystkich wypozyczeń użytkownika???? Historia wypozyczeń ??
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # nie wiem czy tak jest dobrze? User czy Profile?
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    items = models.ManyToManyField(OrderItem)

    def __str__(self):
        return f'{self.user.username}'

