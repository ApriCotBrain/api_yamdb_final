from rest_framework import mixins, filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAdminUser)

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)
from reviews.models import Genre, Category, Title


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

