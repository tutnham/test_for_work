"""
Reusable validators for the Music Catalog API.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime


def validate_release_year(value):
    """
    Validate that the release year is not in the future.
    
    Args:
        value: The year to validate
        
    Raises:
        ValidationError: If the year is in the future
    """
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(
            _('Год выпуска не может быть в будущем.'),
            params={'value': value},
        )


def validate_track_number(value):
    """
    Validate that the track number is positive and reasonable.
    
    Args:
        value: The track number to validate
        
    Raises:
        ValidationError: If the track number is invalid
    """
    if value <= 0:
        raise ValidationError(
            _('Номер трека должен быть положительным числом.'),
            params={'value': value},
        )
    
    if value > 999:
        raise ValidationError(
            _('Номер трека не может быть больше 999.'),
            params={'value': value},
        )


def validate_artist_name(value):
    """
    Validate artist name format and length.
    
    Args:
        value: The artist name to validate
        
    Raises:
        ValidationError: If the name is invalid
    """
    if len(value.strip()) < 2:
        raise ValidationError(
            _('Имя исполнителя должно содержать минимум 2 символа.'),
            params={'value': value},
        )
    
    if len(value) > 200:
        raise ValidationError(
            _('Имя исполнителя не может быть длиннее 200 символов.'),
            params={'value': value},
        )


def validate_song_title(value):
    """
    Validate song title format and length.
    
    Args:
        value: The song title to validate
        
    Raises:
        ValidationError: If the title is invalid
    """
    if len(value.strip()) < 1:
        raise ValidationError(
            _('Название песни не может быть пустым.'),
            params={'value': value},
        )
    
    if len(value) > 200:
        raise ValidationError(
            _('Название песни не может быть длиннее 200 символов.'),
            params={'value': value},
        )


def validate_album_title(value):
    """
    Validate album title format and length.
    
    Args:
        value: The album title to validate
        
    Raises:
        ValidationError: If the title is invalid
    """
    if len(value.strip()) < 1:
        raise ValidationError(
            _('Название альбома не может быть пустым.'),
            params={'value': value},
        )
    
    if len(value) > 200:
        raise ValidationError(
            _('Название альбома не может быть длиннее 200 символов.'),
            params={'value': value},
        )