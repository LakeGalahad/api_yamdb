import random
import string

from rest_framework import viewsets, filters, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin


class RegisterView(APIView):
    """Регистрация пользователя по email и генерация кода."""
    def post(self, request):
        email = request.data.get('email')
        is_user = User.objects.filter(email=email).exists()
        confirm_code = ''.join(
                random.choices(
                    string.digits + string.ascii_uppercase, k=62
                ))
        if is_user:
            user = User.objects.get(email=email)
            serializer = UserSerializer(
                user, data={'confirmation_code': confirm_code}, partial=True
            )
        else:
            username = email[:email.find('@')]
            data = {
                'email': email,
                'confirmation_code': confirm_code,
                'username': username
            }
            serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail('Регистрация на YaMDB', f'Ваш код: {confirm_code}',
                  'webmaster@yamdb.com', [email], fail_silently=False)
        return Response({'email': email})


class TokenView(APIView):
    """Получения токена по email и коду доступа."""
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        email = request.data.get('email')
        confirm_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if user.confirmation_code == confirm_code:
            response = {'token': self.get_token(user)}
            return Response(response, status=status.HTTP_200_OK)
        response = {'confirmation_code': 'Неверный код для данного email'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        """Получение и редактирования своих данных"""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
