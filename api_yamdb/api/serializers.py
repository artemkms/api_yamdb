from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from reviews.models import Category, Genre, Title, User, Comment, Review


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для работы с пользователями при регистрации.
    Валидирует создание пользователя с именем "me".
    """

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Невозможно создать пользователя с таким именем'
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для работы с токенами.
    """

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        extra_kwargs = {
            'username': {
                'validators': []
            }
        }

    def validate(self, data):
        username = data['username']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Код подтверждения не верен')
        return data


class UserSerializer(SignUpSerializer):
    """
    Сериалайзер для работы с пользователями.
    Валидирует создание пользователя с именем "me".
    """

    class Meta:
        model = User
        fields = SignUpSerializer.Meta.fields + (
            'first_name', 'last_name', 'bio', 'role'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name', 'slug'
        )
        model = Category
        lookup_field = 'slug'


class GenresSerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        model = Genre


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
        return round(rating, 2) if rating else rating


class TitlesPOSTSerializer(TitlesSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=False
    )

    class Meta(TitlesSerializer.Meta):
        pass


class ReviewSerializer(serializers.ModelSerializer):
    """Ревью для произведений"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    score = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['title']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            user = self.context['request'].user
            if user.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Комментарии на отзывы"""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
