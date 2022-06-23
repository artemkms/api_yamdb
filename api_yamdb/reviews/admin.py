from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import (User, Title, Category, Genre,
                     GenreTitle, Comment, Review)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'role', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_superuser',
                    'confirmation_code')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
