"""
Database configuration settings for SQLAlchemy connection pool and 
retry mechanism.

Configuration is loaded from environment variables with fallback defaults:

Database:
    DATABASE_NAME: Path to SQLite database file (default: 'data/lafs.db')

Connection Pool:
    POOL_SIZE: Maximum number of persistent connections (default: 15)
    MAX_OVERFLOW: Maximum number of connections above POOL_SIZE (default: 5)
    POOL_TIMEOUT: Seconds to wait for available connection (default: 30)
    POOL_RECYCLE: Seconds before connection is recycled (default: 1800)
    ECHO: Enable SQLAlchemy engine logging (default: False)

Retry Settings:
    MAX_RETRIES: Maximum retry attempts for failed operations (default: 3)
    BASE_DELAY: Initial delay between retries in seconds (default: 1)
    MAX_DELAY: Maximum delay between retries in seconds (default: 10)
"""

import os









# Database
DATABASE_NAME = os.getenv("DATABASE_NAME", "data/lafs.db")

# Connection pool settings
POOL_SIZE = int(os.getenv("POOL_SIZE", "15"))
MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", "5"))
POOL_TIMEOUT = int(os.getenv("POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("POOL_RECYCLE", "1800"))
ECHO = os.getenv("ECHO", "False").lower() == "true"

# Retry settings
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
BASE_DELAY = int(os.getenv("BASE_DELAY", "1"))
MAX_DELAY = int(os.getenv("MAX_DELAY", "10"))
