from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, GenreViewSet,
                       TitleViewSet, CommentViewSet, ReviewsViewSet)

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews',
    ReviewsViewSet, basename='reviews')
v1_router.register(
    r'reviews/(?P<review_id>[1-9]\d*)/comments',
    CommentViewSet, basename='comment')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]

# юрсы решил добавить как были в проекте нашего 9-го спринта,
# но по тз долнжы быть path запросы, есть пара вопросов по этому пункту
