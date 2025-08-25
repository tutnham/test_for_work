"""
URL configuration for the music app.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ArtistViewSet, AlbumViewSet, SongViewSet, AlbumSongViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'songs', SongViewSet, basename='song')
router.register(r'album-songs', AlbumSongViewSet, basename='album-song')

urlpatterns = router.urls