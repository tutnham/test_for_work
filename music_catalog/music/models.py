"""
Music catalog models for the API.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.validators import (
    validate_release_year,
    validate_track_number,
    validate_artist_name,
    validate_song_title,
    validate_album_title
)


class Artist(models.Model):
    """
    Artist model representing a music artist or band.
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Имя исполнителя'),
        help_text=_('Введите имя исполнителя или группы'),
        validators=[validate_artist_name]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        verbose_name = _('Исполнитель')
        verbose_name_plural = _('Исполнители')
        ordering = ['name']
        db_table = 'music_artist'

    def __str__(self):
        return self.name

    def clean(self):
        """Additional model-level validation."""
        super().clean()
        if self.name:
            self.name = self.name.strip()


class Song(models.Model):
    """
    Song model representing a music track.
    """
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название песни'),
        help_text=_('Введите название песни'),
        validators=[validate_song_title]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        verbose_name = _('Песня')
        verbose_name_plural = _('Песни')
        ordering = ['title']
        db_table = 'music_song'

    def __str__(self):
        return self.title

    def clean(self):
        """Additional model-level validation."""
        super().clean()
        if self.title:
            self.title = self.title.strip()


class Album(models.Model):
    """
    Album model representing a music album.
    """
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название альбома'),
        help_text=_('Введите название альбома'),
        validators=[validate_album_title]
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name=_('Исполнитель'),
        help_text=_('Выберите исполнителя')
    )
    release_year = models.IntegerField(
        verbose_name=_('Год выпуска'),
        help_text=_('Введите год выпуска альбома'),
        validators=[validate_release_year]
    )
    songs = models.ManyToManyField(
        Song,
        through='AlbumSong',
        related_name='album_appearances',
        verbose_name=_('Песни'),
        help_text=_('Выберите песни для альбома')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        verbose_name = _('Альбом')
        verbose_name_plural = _('Альбомы')
        ordering = ['-release_year', 'title']
        db_table = 'music_album'

    def __str__(self):
        return f"{self.title} - {self.artist.name} ({self.release_year})"

    def clean(self):
        """Additional model-level validation."""
        super().clean()
        if self.title:
            self.title = self.title.strip()


class AlbumSong(models.Model):
    """
    Through model for the many-to-many relationship between Album and Song.
    This allows the same song to appear in multiple albums with different track numbers.
    """
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='tracks',
        verbose_name=_('Альбом'),
        help_text=_('Выберите альбом')
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='album_appearances',
        verbose_name=_('Песня'),
        help_text=_('Выберите песню')
    )
    track_number = models.PositiveSmallIntegerField(
        verbose_name=_('Номер трека'),
        help_text=_('Введите номер трека в альбоме'),
        validators=[validate_track_number]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        verbose_name = _('Трек альбома')
        verbose_name_plural = _('Треки альбомов')
        ordering = ['album', 'track_number']
        unique_together = [
            ['album', 'track_number'],  # No duplicate track numbers within an album
            ['album', 'song']           # No duplicate songs in the same album
        ]
        db_table = 'music_album_song'

    def __str__(self):
        return f"{self.album.title} - {self.track_number}. {self.song.title}"

    def clean(self):
        """Additional model-level validation."""
        super().clean()
        # Check if track number already exists for this album
        if self.pk is None:  # Only for new instances
            existing_track = AlbumSong.objects.filter(
                album=self.album,
                track_number=self.track_number
            ).exclude(pk=self.pk).first()
            
            if existing_track:
                raise ValidationError({
                    'track_number': _(
                        f'Трек с номером {self.track_number} уже существует в этом альбоме.'
                    )
                })

    def save(self, *args, **kwargs):
        """Override save to ensure validation."""
        self.full_clean()
        super().save(*args, **kwargs)