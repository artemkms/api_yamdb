from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User, Title, Category, Genre, GenreTitle


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'role', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_superuser')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)

