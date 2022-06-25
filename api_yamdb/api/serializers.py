from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import User


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


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для работы с пользователями.
    Валидирует создание пользователя с именем "me".
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Невозможно создать пользователя с таким именем'
            )
        return value
