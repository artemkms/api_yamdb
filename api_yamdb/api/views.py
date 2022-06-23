from random import randint as create_code

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import SignUpSerializer


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


def send_confirmation_code(user, code):
    subject = 'Код подтверждения YaMDb'
    message = f'{code} - ваш код для авторизации на YaMDb'
    admin_email = 'viator3m@yamdb.com'
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)
