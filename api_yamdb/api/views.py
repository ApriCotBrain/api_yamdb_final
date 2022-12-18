from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import mixins, filters, viewsets, generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from rest_framework.decorators import action, api_view, permission_classes

from .permissions import IsAdmin, IsAdminOrReadOnly, HasRoleOrReadOnly

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    GetTokenSerializer,
    UserRegSerializer,
    UserMeSerializer
)
from reviews.models import Genre, Category, Title, Review
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False, methods=['GET', 'PATCH'], url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Предоставлен неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )

class UserRegAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        email_info = (
            f'Здравствуйте {user.username}'
            f'\n Ваш проверочный код для завершения регистрации:'
            f'{confirmation_code}'
        )
        data = {
            'email_info': email_info,
            'to_email': user.email,
            'mail_subject': 'Код подтверждения для регистрации на сайте YaMDB'
        }
        self.__send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def __send_email(data):
        email = EmailMessage(
            subject=data['mail_subject'],
            body=data['email_info'],
            to=[data['to_email']]
        )
        email.send()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, )
    # права на создание только у админа
    pagination_class = LimitOffsetPagination
    # нужен ли, по ТЗ не вижу такого требования
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'category', 'genre', 'year')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    # права на создание только у админа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    # права на создание только у админа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [HasRoleOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [HasRoleOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
