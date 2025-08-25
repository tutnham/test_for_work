"""
API v1 URL configuration for Music Catalog API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from music.views import ArtistViewSet, AlbumViewSet, SongViewSet, AlbumSongViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'songs', SongViewSet, basename='song')
router.register(r'album-songs', AlbumSongViewSet, basename='album-song')

# JWT authentication URLs
jwt_urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # JWT authentication
    path('auth/', include(jwt_urlpatterns)),
    
    # API root
    path('', include('rest_framework.urls')),
]