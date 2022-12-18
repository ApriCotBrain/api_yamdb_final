from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, GenreViewSet,
                       TitleViewSet, CommentViewSet, ReviewViewSet, UserViewSet, GetTokenAPIView, UserRegAPIView)

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

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path(
        'v1/auth/token/', GetTokenAPIView.as_view(), name='get_token'
    ),
    path(
        'v1/auth/signup/', UserRegAPIView.as_view(), name='signup'
    ),

]
