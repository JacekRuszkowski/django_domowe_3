from django.db import models
from django.urls import reverse
from PIL import Image


# Atrybuty modelu książki:
# 1. Tytuł
# 2. Autor
# 3. Zdjęcie książki
# 4. Opis
# 5. Ilość stron
# 6. Kategoria (książki mają należeć do jednej kategorii?)
# 7. Czy jest dostępna (to ma się zmieniać w zależności od tego czy ktoż wypozyczył).
# 8. Czas wypozyczenia - czy to tutaj?

# Wymyślić jak podłączyc model książki do kategorii.
# 1. Stowrzyć model kategorii
# 2. Przypisać książke do kategorii (za pomocę foreign Key? nr id kategorii?)


# kategoria
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        unique_together = ('slug', 'parent_category', )
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
    is_available = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        img.save(self.image.path)

