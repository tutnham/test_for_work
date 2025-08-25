"""
Custom pagination classes for the Music Catalog API.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class with customizable page size.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """
        Return a paginated response with metadata.
        
        Args:
            data: The paginated data
            
        Returns:
            Response: Paginated response with metadata
        """
        return Response({
            'success': True,
            'message': 'Success',
            'data': data,
            'pagination': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.get_page_size(self.request),
            }
        })


class LargeResultsSetPagination(PageNumberPagination):
    """
    Pagination class for large result sets.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200