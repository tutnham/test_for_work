"""
Views for the Music Catalog API.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _

from .models import Artist, Album, Song, AlbumSong
from .serializers import (
    ArtistSerializer, ArtistDetailSerializer,
    AlbumSerializer, AlbumDetailSerializer, AlbumCreateUpdateSerializer,
    SongSerializer, SongDetailSerializer,
    AlbumSongSerializer
)
from core.responses import success_response, error_response


class ArtistViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Artist model with CRUD operations.
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return ArtistDetailSerializer
        return ArtistSerializer
    
    def get_queryset(self):
        """Optimize queryset with related data."""
        return Artist.objects.prefetch_related('albums').all()
    
    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        """Get all albums for a specific artist."""
        artist = self.get_object()
        albums = artist.albums.all()
        serializer = AlbumSerializer(albums, many=True)
        return success_response(
            data=serializer.data,
            message=_('Альбомы исполнителя получены успешно')
        )
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get artists with most albums."""
        artists = Artist.objects.annotate(
            albums_count=Count('albums')
        ).filter(albums_count__gt=0).order_by('-albums_count')[:10]
        
        serializer = self.get_serializer(artists, many=True)
        return success_response(
            data=serializer.data,
            message=_('Популярные исполнители получены успешно')
        )


class AlbumViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Album model with CRUD operations.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['artist', 'release_year']
    search_fields = ['title', 'artist__name']
    ordering_fields = ['title', 'release_year', 'created_at', 'updated_at']
    ordering = ['-release_year', 'title']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['retrieve', 'list']:
            return AlbumDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AlbumCreateUpdateSerializer
        return AlbumSerializer
    
    def get_queryset(self):
        """Optimize queryset with related data."""
        return Album.objects.select_related('artist').prefetch_related(
            'tracks__song'
        ).all()
    
    def create(self, request, *args, **kwargs):
        """Create album with tracks."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = serializer.save()
        
        response_serializer = AlbumDetailSerializer(album)
        return success_response(
            data=response_serializer.data,
            message=_('Альбом создан успешно'),
            status_code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Update album with tracks."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        album = serializer.save()
        
        response_serializer = AlbumDetailSerializer(album)
        return success_response(
            data=response_serializer.data,
            message=_('Альбом обновлен успешно')
        )
    
    @action(detail=True, methods=['get'])
    def tracks(self, request, pk=None):
        """Get all tracks for a specific album."""
        album = self.get_object()
        tracks = album.tracks.all()
        serializer = AlbumSongSerializer(tracks, many=True)
        return success_response(
            data=serializer.data,
            message=_('Треки альбома получены успешно')
        )
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent albums."""
        albums = Album.objects.order_by('-created_at')[:10]
        serializer = self.get_serializer(albums, many=True)
        return success_response(
            data=serializer.data,
            message=_('Недавние альбомы получены успешно')
        )
    
    @action(detail=False, methods=['get'])
    def by_year(self, request):
        """Get albums grouped by year."""
        year = request.query_params.get('year')
        if not year:
            return error_response(
                message=_('Параметр year обязателен'),
                error_code='MISSING_YEAR_PARAMETER'
            )
        
        try:
            year = int(year)
        except ValueError:
            return error_response(
                message=_('Год должен быть числом'),
                error_code='INVALID_YEAR_FORMAT'
            )
        
        albums = Album.objects.filter(release_year=year)
        serializer = self.get_serializer(albums, many=True)
        return success_response(
            data=serializer.data,
            message=_('Альбомы за {} год получены успешно').format(year)
        )


class SongViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Song model with CRUD operations.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['title']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return SongDetailSerializer
        return SongSerializer
    
    def get_queryset(self):
        """Optimize queryset with related data."""
        return Song.objects.prefetch_related('album_appearances__album').all()
    
    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        """Get all albums where this song appears."""
        song = self.get_object()
        albums = Album.objects.filter(tracks__song=song).distinct()
        serializer = AlbumSerializer(albums, many=True)
        return success_response(
            data=serializer.data,
            message=_('Альбомы с этой песней получены успешно')
        )
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get songs that appear in most albums."""
        songs = Song.objects.annotate(
            appearances_count=Count('album_appearances')
        ).filter(appearances_count__gt=0).order_by('-appearances_count')[:10]
        
        serializer = self.get_serializer(songs, many=True)
        return success_response(
            data=serializer.data,
            message=_('Популярные песни получены успешно')
        )
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search for songs."""
        query = request.query_params.get('q', '')
        if not query:
            return error_response(
                message=_('Параметр поиска q обязателен'),
                error_code='MISSING_SEARCH_PARAMETER'
            )
        
        songs = Song.objects.filter(
            Q(title__icontains=query) |
            Q(album_appearances__album__title__icontains=query) |
            Q(album_appearances__album__artist__name__icontains=query)
        ).distinct()
        
        serializer = self.get_serializer(songs, many=True)
        return success_response(
            data=serializer.data,
            message=_('Результаты поиска получены успешно')
        )


class AlbumSongViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AlbumSong through model.
    """
    queryset = AlbumSong.objects.all()
    serializer_class = AlbumSongSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['album', 'song']
    ordering_fields = ['track_number', 'created_at', 'updated_at']
    ordering = ['album', 'track_number']
    
    def get_queryset(self):
        """Optimize queryset with related data."""
        return AlbumSong.objects.select_related('album', 'song').all()
    
    def create(self, request, *args, **kwargs):
        """Create album track with validation context."""
        serializer = self.get_serializer(
            data=request.data,
            context={'album_id': request.data.get('album')}
        )
        serializer.is_valid(raise_exception=True)
        album_song = serializer.save()
        
        return success_response(
            data=serializer.data,
            message=_('Трек добавлен в альбом успешно'),
            status_code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Update album track with validation context."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={'album_id': instance.album.id}
        )
        serializer.is_valid(raise_exception=True)
        album_song = serializer.save()
        
        return success_response(
            data=serializer.data,
            message=_('Трек обновлен успешно')
        )