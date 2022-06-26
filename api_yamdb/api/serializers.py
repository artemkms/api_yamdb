from django.db.models import Avg


from rest_framework import serializers


from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name', 'slug'
        )
        model = Category
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name', 'slug'
        )
        model = Genre
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    genre = GenresSerializer(many=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'category',
            'genre', 'description', 'rating'
        )
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(
            Avg('score')).get('score__avg')
        if not rating:
            return rating
        return round(rating, 2)

    # def validate(self, data):
    #     print('Валидация была')
    #     return data


class TitlesPOSTSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all()
                                            )
    genre = serializers.SlugRelatedField(slug_field='slug',
                                          queryset=Genre.objects.all(),
                                          many = True,
                                          required=False
                                          )

    class Meta:
        fields = (
            'id', 'name', 'year', 'category',
            'genre', 'description', 'rating'
        )
        model = Title

    # def validate(self, data):
    #     print('Валидация была')
    #     return data

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(
            Avg('score')).get('score__avg')
        if not rating:
            return rating
        return round(rating, 2)
