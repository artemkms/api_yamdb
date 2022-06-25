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
