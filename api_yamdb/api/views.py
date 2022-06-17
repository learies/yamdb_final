from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title
from users.models import User

from .filters import TitleFilter
from .mixins import CategoryGenreModelMixin
from .paginations import PageNumberPagination
from .permissions import (AdminOnly, IsAdminOrReadOnly,
                          UserAndModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleSerializer, TitlesViewSerializer,
                          TokenSerializer, UserNotAdminSerializer,
                          UserSerializer)


class APIGetToken(APIView):
    """Получить токен по confirmation_code пользователя"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if data.get('confirmation_code') != user.confirmation_code:
            return Response(
                {'confirmation_code': 'Неверный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = RefreshToken.for_user(user).access_token
        return Response(
            {'token': str(token)},
            status=status.HTTP_201_CREATED,
        )


class APISignup(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Привет, {user.username}!'
            f'\nКод доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код для доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('username')
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    user, data=request.data, partial=True,
                )
            else:
                serializer = UserNotAdminSerializer(
                    user, data=request.data, partial=True,
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserNotAdminSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CategoryGenreModelMixin):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreModelMixin):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (UserAndModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (UserAndModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('Нет такого отзыва')
        return review.comments.all().order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('Нет такого отзыва')
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_queryset(self):
        return Title.objects.all().annotate(
            _rating=Avg('reviews__score')
        ).order_by('id')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesViewSerializer
        return TitleSerializer
