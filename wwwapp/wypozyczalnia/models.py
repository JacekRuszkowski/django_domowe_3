from django.db import models

# Atrybuty modelu książki:
# 1. Tytuł
# 2. Autor
# 3. Zdjęcie książki
# 4. Opis
# 5. Ilość stron
# 6. Kategoria (książki mają należeć do jednej kategorii?)
# 7. Czy jest dostępna (to ma się zmieniać w zależności od tego czy ktoż wypozyczył).
# 8. Czas wypozyczenia - czy to tutaj?


class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    description = models.TextField()
    pages = models.CharField(max_length=5)
    image = models.ImageField(default='default.jpg', upload_to='book_images')
    is_available = models.BooleanField()
    # category = ?????

    def __str__(self):
        return self.title