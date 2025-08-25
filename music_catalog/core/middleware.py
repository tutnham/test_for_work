"""
Custom middleware for the Music Catalog API.
"""

import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log API requests and response times.
    """
    
    def process_request(self, request):
        """Log the start of request processing."""
        request.start_time = time.time()
        
        # Log API requests
        if request.path.startswith('/api/'):
            logger.info(f"API Request: {request.method} {request.path}")
    
    def process_response(self, request, response):
        """Log the end of request processing."""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log API responses
            if request.path.startswith('/api/'):
                logger.info(
                    f"API Response: {request.method} {request.path} "
                    f"- {response.status_code} ({duration:.3f}s)"
                )
        
        return response