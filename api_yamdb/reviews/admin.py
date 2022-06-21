from django.contrib import admin

# Register your models here.
from .models import Title, Category, Genre, GenreTitle

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
