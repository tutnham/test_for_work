"""
Serializers for the Music Catalog API.
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Artist, Album, Song, AlbumSong


class ArtistSerializer(serializers.ModelSerializer):
    """
    Serializer for the Artist model.
    """
    albums_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = [
            'id', 'name', 'albums_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_albums_count(self, obj):
        """Get the number of albums for this artist."""
        return obj.albums.count()


class SongSerializer(serializers.ModelSerializer):
    """
    Serializer for the Song model.
    """
    album_appearances_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = [
            'id', 'title', 'album_appearances_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_album_appearances_count(self, obj):
        """Get the number of albums this song appears in."""
        return obj.album_appearances.count()


class AlbumSongSerializer(serializers.ModelSerializer):
    """
    Serializer for the AlbumSong through model.
    """
    song = SongSerializer(read_only=True)
    song_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = AlbumSong
        fields = [
            'id', 'track_number', 'song', 'song_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        """Validate track number uniqueness within album."""
        album = self.context.get('album')
        track_number = attrs.get('track_number')
        song_id = attrs.get('song_id')
        
        if album and track_number:
            # Check if track number already exists for this album
            existing_track = AlbumSong.objects.filter(
                album=album,
                track_number=track_number
            )
            
            if self.instance:
                existing_track = existing_track.exclude(pk=self.instance.pk)
            
            if existing_track.exists():
                raise serializers.ValidationError({
                    'track_number': _(
                        f'Трек с номером {track_number} уже существует в этом альбоме.'
                    )
                })
        
        if album and song_id:
            # Check if song already exists in this album
            existing_song = AlbumSong.objects.filter(
                album=album,
                song_id=song_id
            )
            
            if self.instance:
                existing_song = existing_song.exclude(pk=self.instance.pk)
            
            if existing_song.exists():
                raise serializers.ValidationError({
                    'song_id': _('Эта песня уже добавлена в альбом.')
                })
        
        return attrs


class AlbumSerializer(serializers.ModelSerializer):
    """
    Serializer for the Album model with nested tracks.
    """
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.IntegerField(write_only=True)
    tracks = AlbumSongSerializer(many=True, read_only=True)
    tracks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Album
        fields = [
            'id', 'title', 'artist', 'artist_id', 'release_year',
            'tracks', 'tracks_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_tracks_count(self, obj):
        """Get the number of tracks in this album."""
        return obj.tracks.count()
    
    def validate_artist_id(self, value):
        """Validate that the artist exists."""
        try:
            Artist.objects.get(pk=value)
        except Artist.DoesNotExist:
            raise serializers.ValidationError(_('Исполнитель не найден.'))
        return value


class AlbumDetailSerializer(AlbumSerializer):
    """
    Detailed serializer for Album with full track information.
    """
    class Meta(AlbumSerializer.Meta):
        fields = AlbumSerializer.Meta.fields


class AlbumCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating albums with tracks.
    """
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.IntegerField(write_only=True)
    tracks = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Album
        fields = [
            'id', 'title', 'artist', 'artist_id', 'release_year',
            'tracks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_artist_id(self, value):
        """Validate that the artist exists."""
        try:
            Artist.objects.get(pk=value)
        except Artist.DoesNotExist:
            raise serializers.ValidationError(_('Исполнитель не найден.'))
        return value
    
    def validate_tracks(self, value):
        """Validate tracks data."""
        if not value:
            return value
        
        track_numbers = []
        song_ids = []
        
        for track_data in value:
            track_number = track_data.get('track_number')
            song_id = track_data.get('song_id')
            
            if not track_number:
                raise serializers.ValidationError(_('Номер трека обязателен.'))
            
            if not song_id:
                raise serializers.ValidationError(_('ID песни обязателен.'))
            
            # Check for duplicate track numbers
            if track_number in track_numbers:
                raise serializers.ValidationError(
                    _('Дублирующиеся номера треков не допускаются.')
                )
            
            # Check for duplicate songs
            if song_id in song_ids:
                raise serializers.ValidationError(
                    _('Дублирующиеся песни не допускаются.')
                )
            
            track_numbers.append(track_number)
            song_ids.append(song_id)
            
            # Validate that song exists
            try:
                Song.objects.get(pk=song_id)
            except Song.DoesNotExist:
                raise serializers.ValidationError(
                    _('Песня с ID {} не найдена.').format(song_id)
                )
        
        return value
    
    def create(self, validated_data):
        """Create album with tracks."""
        tracks_data = validated_data.pop('tracks', [])
        album = Album.objects.create(**validated_data)
        
        # Create tracks
        for track_data in tracks_data:
            AlbumSong.objects.create(
                album=album,
                song_id=track_data['song_id'],
                track_number=track_data['track_number']
            )
        
        return album
    
    def update(self, instance, validated_data):
        """Update album with tracks."""
        tracks_data = validated_data.pop('tracks', None)
        
        # Update album fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update tracks if provided
        if tracks_data is not None:
            # Remove existing tracks
            instance.tracks.all().delete()
            
            # Create new tracks
            for track_data in tracks_data:
                AlbumSong.objects.create(
                    album=instance,
                    song_id=track_data['song_id'],
                    track_number=track_data['track_number']
                )
        
        return instance


class ArtistDetailSerializer(ArtistSerializer):
    """
    Detailed serializer for Artist with albums information.
    """
    albums = AlbumSerializer(many=True, read_only=True)
    
    class Meta(ArtistSerializer.Meta):
        fields = ArtistSerializer.Meta.fields + ['albums']


class SongDetailSerializer(SongSerializer):
    """
    Detailed serializer for Song with album appearances information.
    """
    album_appearances = AlbumSongSerializer(many=True, read_only=True)
    
    class Meta(SongSerializer.Meta):
        fields = SongSerializer.Meta.fields + ['album_appearances']