from django.db import models

# Create your models here.
class Title(models.Model):
    name = models.TextField()
    year = models.DateTimeField(input_formats='%y')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genres = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
        related_name='titles'
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'], name='unique_GenreTitle'
            ),
        ]

    def __str__(self):
        return f'За произведением {self.title} закреплен жанр {self.genre}'