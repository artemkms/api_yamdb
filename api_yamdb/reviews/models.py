from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_superuser:
            self.role = 'admin'

    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ'),
    )

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=250,
    )
    bio = models.TextField(
        verbose_name='Описание',
        blank=True,
        max_length=250,
    )
    role = models.CharField(
        verbose_name='Роль',
        default='user',
        choices=ROLES,
        max_length=16,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        blank=True,
        max_length=50
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user'
            )
        ]


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