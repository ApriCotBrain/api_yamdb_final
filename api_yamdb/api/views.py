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
from reviews.models import Genre, Category, Title, Reviews, Comment


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


class ReviewsViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializers

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = CommentSerializers
    queryset = Comment.objects.all()

    def get_reviews(self):
        return get_object_or_404(Reviews, pk=self.kwargs.get('reviews_id'))

# вьюхи пока накидал такие, если вы не против, послезавтра у меня фулл
# ночь и день свободны будут, переделаю, поищу ещё в документации, по
# mixins есть предположение что я слишком много их указал, по сути все))
# но по логике как раз все они и нужны, возможно ошибаюсь, тоже с радостью
# услышал вашу точку зрения по поводу mixinов
