"""
Logging utilities for the Music Catalog API.
"""

import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    """
    
    def format(self, record):
        """Format log record as JSON."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry)


def setup_logging():
    """
    Setup logging configuration for the application.
    """
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure API logger
    api_logger = logging.getLogger('music_catalog.api')
    api_logger.setLevel(logging.INFO)
    
    # Add JSON formatter for API logs
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(JSONFormatter())
    api_logger.addHandler(json_handler)
    
    return api_logger