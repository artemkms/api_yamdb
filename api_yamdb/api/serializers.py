from rest_framework import serializers

from reviews.models import User


class SignUpSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        extra_kwargs = {
            'username': {
                'validators': []
            }
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    # FIXME: Разобраться с запретом юзеру изменять свою роль. Почему пустой контекст?
    # def validate(self, data):
    #     user = self.context.get('request').user
    #     if user.role == 'user' and 'role' in data.keys():
    #         raise serializers.ValidationError('Невозможно изменить свою роль')
    #     return data

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Невозможно создать пользователя с таким именем'
            )
        return value
