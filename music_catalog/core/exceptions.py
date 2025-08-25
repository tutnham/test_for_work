"""
Custom exception handler for the Music Catalog API.
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from .responses import error_response, validation_error_response, not_found_response

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses.
    
    Args:
        exc: The exception that was raised
        context: The context in which the exception occurred
        
    Returns:
        Response: Standardized error response
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Log the exception
        logger.error(f"API Exception: {exc} in {context['view'].__class__.__name__}")
        
        # Customize the response format
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                return validation_error_response(
                    errors=exc.detail,
                    message=str(exc),
                    error_code="VALIDATION_ERROR"
                )
            else:
                return error_response(
                    message=str(exc.detail),
                    error_code="API_ERROR",
                    status_code=response.status_code
                )
    
    # Handle Django-specific exceptions
    if isinstance(exc, Http404):
        return not_found_response(
            message=_("Запрашиваемый ресурс не найден"),
            error_code="NOT_FOUND"
        )
    
    if isinstance(exc, ValidationError):
        errors = {}
        if hasattr(exc, 'message_dict'):
            errors = exc.message_dict
        else:
            errors = {'non_field_errors': [str(exc)]}
        
        return validation_error_response(
            errors=errors,
            message=_("Ошибка валидации данных"),
            error_code="VALIDATION_ERROR"
        )
    
    # Handle unexpected exceptions
    logger.error(f"Unexpected exception: {exc} in {context['view'].__class__.__name__}")
    
    return error_response(
        message=_("Внутренняя ошибка сервера"),
        error_code="INTERNAL_ERROR",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )