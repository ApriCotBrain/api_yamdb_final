from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import mixins, filters, viewsets, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from .permissions import IsAdmin, IsAdminOrReadOnly, HasRoleOrReadOnly
import django_filters.rest_framework

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    CreateTitleSerializer,
    ShowTitleSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer
)
from reviews.models import Genre, Category, Title, Review
from users.models import User
from api.filters import TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg("reviews__score")
    ).order_by("name")
    serializer_class = ShowTitleSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    #filterset_class = (TitleFilter,)
    #filterset_class_fields = ('slug',)
    search_fields = ('name', 'category', 'genre', 'year')
    #filter_fields = ('slug',)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return CreateTitleSerializer
        return ShowTitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ('name', )
    lookup_field = 'slug'

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
