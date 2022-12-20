import django_filters.rest_framework
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import User
from api.filters import TitleFilter
from api.serializers import (CategorySerializer, CommentSerializer,
                             CreateTitleSerializer, GenreSerializer,
                             GetTokenSerializer, ReviewSerializer,
                             ShowTitleSerializer, UserMeSerializer,
                             UserRegSerializer, UserSerializer)

from .permissions import HasRoleOrReadOnly, IsAdmin, IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'delete', 'patch']

    @action(
        methods=['GET', 'PATCH'], url_path='me', detail=False,
        permission_classes=(IsAuthenticated,)
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
        email = request.data.get('email')
        username = request.data.get('username')
        if User.objects.filter(email=email).exists():
            if not User.objects.filter(username=username).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if (User.objects.filter(username=username).exists()
           or User.objects.filter(email=email).exists()):
            serializer = UserRegSerializer(data=request.data)
            return Response(serializer.initial_data, status=status.HTTP_200_OK)
        serializer = UserRegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
        )
        confirmation_code = default_token_generator.make_token(user)
        email_text = (
            'Ваш код для завершения регистрации: '
            f'{confirmation_code}'
        )
        data = {
            'email_info': email_text,
            'to_email': user.email,
            'mail_subject': 'Код подтверждения YaMDB'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['mail_subject'],
            body=data['email_info'],
            from_email=settings.EMAIL_FROM,
            to=[data['to_email']]
        )
        email.send()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg("reviews__score")
    ).order_by("name")
    serializer_class = ShowTitleSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('genre__slug', 'name')
    search_fields = ('name', 'category', 'genre', 'year')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return CreateTitleSerializer
        return ShowTitleSerializer


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    ordering = ('name',)


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet,):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


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
