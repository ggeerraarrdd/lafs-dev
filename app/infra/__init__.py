"""
Infrastructure module for application.

This module provides core infrastructure components including:
- Database management and connection pooling
- Logging configuration
- Configuration management
- External service integrations

Main Components:
    DatabaseManager: Handles database connections, pooling, and operations
                    with automatic retries and connection management.

Configuration is handled through environment variables with sensible defaults.
See config/ directory for detailed configuration options.
"""

from .database_manager import DatabaseManager

# Define what should be available when using "from infra import *"
__all__ = ['DatabaseManager',
           ]
