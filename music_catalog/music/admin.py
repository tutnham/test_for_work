"""
Django admin configuration for the Music Catalog API.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import Artist, Album, Song, AlbumSong


class AlbumSongInline(admin.TabularInline):
    """
    Inline admin for AlbumSong model to manage tracks within albums.
    """
    model = AlbumSong
    extra = 1
    fields = ['song', 'track_number']
    ordering = ['track_number']
    verbose_name = _('Трек')
    verbose_name_plural = _('Треки')
    
    def get_queryset(self, request):
        """Order tracks by track number."""
        return super().get_queryset(request).order_by('track_number')


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    """
    Admin configuration for Artist model.
    """
    list_display = ['name', 'albums_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Метаданные'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def albums_count(self, obj):
        """Display the number of albums for this artist."""
        return obj.albums.count()
    albums_count.short_description = _('Количество альбомов')
    albums_count.admin_order_field = 'albums_count'


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """
    Admin configuration for Song model.
    """
    list_display = ['title', 'album_appearances_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title']
    ordering = ['title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        (_('Метаданные'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def album_appearances_count(self, obj):
        """Display the number of albums this song appears in."""
        return obj.album_appearances.count()
    album_appearances_count.short_description = _('Количество альбомов')
    album_appearances_count.admin_order_field = 'album_appearances_count'


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """
    Admin configuration for Album model with inline tracks management.
    """
    list_display = ['title', 'artist', 'release_year', 'tracks_count', 'created_at']
    list_filter = ['artist', 'release_year', 'created_at', 'updated_at']
    search_fields = ['title', 'artist__name']
    ordering = ['-release_year', 'title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AlbumSongInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'artist', 'release_year')
        }),
        (_('Метаданные'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def tracks_count(self, obj):
        """Display the number of tracks in this album."""
        return obj.tracks.count()
    tracks_count.short_description = _('Количество треков')
    tracks_count.admin_order_field = 'tracks_count'
    
    def get_queryset(self, request):
        """Optimize queryset with related data."""
        return super().get_queryset(request).select_related('artist').prefetch_related('tracks')
    
    def save_formset(self, request, form, formset, change):
        """Handle saving of inline tracks with validation."""
        instances = formset.save(commit=False)
        
        # Validate track numbers
        track_numbers = []
        for instance in instances:
            if hasattr(instance, 'track_number') and instance.track_number:
                if instance.track_number in track_numbers:
                    # Handle duplicate track numbers
                    continue
                track_numbers.append(instance.track_number)
        
        # Save instances
        for instance in instances:
            instance.save()
        
        # Delete marked instances
        for obj in formset.deleted_objects:
            obj.delete()
        
        formset.save_m2m()


@admin.register(AlbumSong)
class AlbumSongAdmin(admin.ModelAdmin):
    """
    Admin configuration for AlbumSong through model.
    """
    list_display = ['album', 'song', 'track_number', 'created_at']
    list_filter = ['album__artist', 'album', 'created_at', 'updated_at']
    search_fields = ['album__title', 'song__title', 'album__artist__name']
    ordering = ['album', 'track_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('album', 'song', 'track_number')
        }),
        (_('Метаданные'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related data."""
        return super().get_queryset(request).select_related('album', 'song', 'album__artist')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Customize foreign key fields."""
        if db_field.name == "album":
            kwargs["queryset"] = Album.objects.select_related('artist').order_by('title')
        elif db_field.name == "song":
            kwargs["queryset"] = Song.objects.order_by('title')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Customize admin site
admin.site.site_header = _('Администрирование музыкального каталога')
admin.site.site_title = _('Музыкальный каталог')
admin.site.index_title = _('Управление музыкальным каталогом')