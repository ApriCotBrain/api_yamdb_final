from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       GetTokenAPIView, ReviewViewSet, TitleViewSet,
                       UserRegAPIView, UserViewSet)

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register('users', UserViewSet, basename='users')

url_auth = [path('token/', GetTokenAPIView.as_view()),
            path('signup/', UserRegAPIView.as_view())]

urlpatterns = [
    path('auth/', include(url_auth)),
    path('', include(v1_router.urls)),
]
