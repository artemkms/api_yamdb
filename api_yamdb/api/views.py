from random import randint as create_code

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsRoleAdmin
from api.serializers import SignUpSerializer, TokenSerializer, UserSerializer
from reviews.models import User


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        code = create_code(100000, 999999)
        user = serializer.save(confirmation_code=code)
        send_confirmation_code(user, code)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        code = serializer.validated_data.get('confirmation_code')
        if user.confirmation_code == code:
            access = AccessToken.for_user(user)
            return Response(f'token: {access}', status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_code(user, code):
    subject = 'Код подтверждения YaMDb'
    message = f'{code} - ваш код для авторизации на YaMDb'
    admin_email = 'viator3m@yamdb.com'
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsRoleAdmin,)
