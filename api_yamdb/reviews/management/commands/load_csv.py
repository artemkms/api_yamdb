import csv

from django.core.management import BaseCommand

from api_yamdb import settings
from reviews.models import (User, Title, Category, Genre,
                            GenreTitle, Comment, Review)

MODELS_FILES = {
    User: 'users.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',

}


# TODO: Разобраться с импортом csv-файлов в базу данных
class Command(BaseCommand):
    def handle(self, *args, **options):
        for model, file in MODELS_FILES.items():
            with open(
                    f'{settings.BASE_DIR}/static/data/{file}',
                    'r', encoding='utf-8',
            ) as table:
                reader = csv.DictReader(table)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('===SUCCESS==='))
