from django.shortcuts import get_object_or_404
from rest_framework import mixins, filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAdminUser)

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializers,
    CommentSerializers
)
from reviews.models import Genre, Category, Title, Reviews, Comments


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminUser, )
    # права на создание только у админа
    pagination_class = LimitOffsetPagination
    # нужен ли, по ТЗ не вижу такого требования
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'category', 'genre', 'year')


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)
    # права на создание только у админа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser,)
    # права на создание только у админа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        review = get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
