from random import randint as create_code

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsRoleAdmin
from api.serializers import SignUpSerializer, TokenSerializer, UserSerializer
from reviews.models import User


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup(request):
    """
    Добавляет нового пользователя в БД.
    Отправляет шестизначный код подтверждения на почту.
    """
    code = create_code(100000, 999999)
    serializer = SignUpSerializer(data=request.data)

    try:
        user = User.objects.get(
            username=serializer.initial_data.get('username'))
        user.confirmation_code=code
        user.save()
        send_confirmation_code(user, code)
        message = {
            "message":
                "Пользователь уже существует. "
                "Код подтверждения отправлен повторно."
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        if serializer.is_valid():
            user = serializer.save(confirmation_code=code)
            send_confirmation_code(user, code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def get_token(request):
    """
    Возвращает пользователю токен для авторизации.
    В качестве параметра принимает объект request.
    """
    serializer = TokenSerializer(data=request.data)
    username = serializer.initial_data.get('username')
    code = serializer.initial_data.get('confirmation_code')
    if serializer.is_valid():
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == code:
            access = AccessToken.for_user(user)
            return Response(f'token: {access}', status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_code(user, code):
    subject = 'YaMDb. Код авторизации.'
    message = f'Здравствуй, {user}! \n' \
              f'Это твой код для авторизации {code}'
    from_email = 'admin@yamdb.com'
    to_email = [user.email]
    return send_mail(subject, message, from_email, to_email)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет работает с эндпойнтом users/.
    Предоставляет администратору доступ ко всем видам запросов.
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsRoleAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class MePage(APIView):
    """
    Реализация доступа к эндпойнту users/me/.
    Get-запрос возвращает пользователю информацию о нем.
    Patch-запрос позволяет редактировать эту информацию.
    Изменить свою пользовательскую роль нельзя.
    """
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
