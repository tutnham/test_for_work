"""
Unified response structures for the Music Catalog API.
"""

from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """
    Create a standardized success response.
    
    Args:
        data: The response data
        message: Success message
        status_code: HTTP status code
    
    Returns:
        Response: Standardized success response
    """
    response_data = {
        "success": True,
        "message": message,
        "data": data
    }
    return Response(response_data, status=status_code)


def error_response(message="Error", errors=None, error_code=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        errors: Field-specific errors
        error_code: Specific error code
        status_code: HTTP status code
    
    Returns:
        Response: Standardized error response
    """
    response_data = {
        "success": False,
        "message": message,
        "errors": errors or {},
        "error_code": error_code
    }
    return Response(response_data, status=status_code)


def not_found_response(message="Resource not found", error_code="NOT_FOUND"):
    """
    Create a standardized 404 response.
    
    Args:
        message: Not found message
        error_code: Error code
    
    Returns:
        Response: 404 response
    """
    return error_response(
        message=message,
        error_code=error_code,
        status_code=status.HTTP_404_NOT_FOUND
    )


def validation_error_response(errors, message="Validation error", error_code="VALIDATION_ERROR"):
    """
    Create a standardized validation error response.
    
    Args:
        errors: Validation errors
        message: Error message
        error_code: Error code
    
    Returns:
        Response: Validation error response
    """
    return error_response(
        message=message,
        errors=errors,
        error_code=error_code,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )