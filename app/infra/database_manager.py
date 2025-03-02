"""
SQLite connection pool and transaction manager. Implements connection pooling, 
transaction management, automatic retry mechanisms, and comprehensive 
monitoring/logging capabilities.

Core Functionality:
- Connection pooling via SQLAlchemy QueuePool
- ACID-compliant transaction management
- Exponential backoff retry mechanism
- Performance monitoring and metrics logging

Technical Features:
- Multi-threaded connection pooling with SQLAlchemy
- Automatic connection recovery and failover
- Query execution time monitoring
- Comprehensive logging with caller tracking
"""

# Python Standard Library
import inspect
import logging  # Runtime logging and monitoring
import time
from typing import Any, Dict, List
from contextlib import contextmanager  # Context management

# Third-Party Libraries
from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool  # Connection pooling
from sqlalchemy.exc import OperationalError  # Exception handling

# Local
from app.config import DATABASE_NAME
from app.config import POOL_SIZE
from app.config import MAX_OVERFLOW
from app.config import POOL_TIMEOUT
from app.config import POOL_RECYCLE
from app.config import ECHO
from app.config import MAX_RETRIES
from app.config import BASE_DELAY
from app.config import MAX_DELAY
from .log import setup_logging


# Initialize logging
setup_logging()

# Set up our diary (logging)
logger = logging.getLogger(__name__)










class DatabaseManager:
    """
    DatabaseManager: Manages SQLite connections with connection pooling and transaction management.
    
    Core Components:
    1. Connection pool management and session handling
    2. ACID-compliant transaction management
    3. Automatic retry mechanism with exponential backoff
    4. Performance monitoring and metrics collection
    """
    def __init__(self):
        """
        Initializes DatabaseManager with connection pool parameters from config.
        
        Args:
            database_path: Path to the SQLite database file
            pool_size: Maximum number of database connections to maintain
            max_overflow: Additional connections allowed when pool is full
            pool_timeout: Seconds to wait for a connection from pool
            pool_recycle: Seconds before a connection is recycled
            echo: If True, logs all SQL activity
            max_retries: Maximum number of connection retry attempts
            base_delay: Initial delay in seconds between retries
            max_delay: Maximum delay in seconds between retries
        """
        # Setting up our database connection (like opening up shop!)
        self.engine = create_engine(
            f'sqlite:///{DATABASE_NAME}',
            poolclass=QueuePool,
            pool_size=POOL_SIZE,              # How many connections we maintain
            max_overflow=MAX_OVERFLOW,        # Extra connections when busy
            pool_timeout=POOL_TIMEOUT,        # How long to wait for a connection
            pool_recycle=POOL_RECYCLE,        # When to refresh connections
            echo=ECHO                         # Whether to log all SQL
        )

        # Retry configuration parameters
        self.max_retries = MAX_RETRIES
        self.base_delay = BASE_DELAY
        self.max_delay = MAX_DELAY

        # Connection event handler with retry logic
        @event.listens_for(self.engine, "connect")
        def handle_connect(dbapi_connection, _connection_record):
            retry_count = 0

            # Implement exponential backoff retry mechanism
            while retry_count < self.max_retries:
                try:
                    return dbapi_connection
                except OperationalError:
                    retry_count += 1
                    if retry_count == self.max_retries:
                        raise  # Maximum retries exceeded
                    # Calculate exponential backoff delay
                    delay = min(self.base_delay * (2 ** (retry_count - 1)), self.max_delay)
                    time.sleep(delay)

        # Initialize session factory
        # This is like our ticket system - it helps organize database requests
        self.Session = sessionmaker(bind=self.engine)


    def get_session(self):
        """
        Returns a new SQLAlchemy session instance.

        This is like getting a ticket to talk to the database.
        """
        return self.Session()


    @contextmanager
    def transaction(self):
        """
        Context manager for ACID-compliant transaction handling.
        
        Implements automatic rollback on exception and
        proper session cleanup.
        
        If anything goes wrong, it undoes all the changes (like ctrl+z)
        If everything goes well, it saves all the changes
        """
        session = self.get_session()

        try:

            yield session
            session.commit()  # Commit transaction

        except Exception as e:

            session.rollback()  # Rollback on exception
            logger.error("Transaction failed: %s", e)
            raise

        finally:
            session.close()  # Release session


    def execute_read_query(self, query: str, parameters: dict = None) -> List[Dict[str, Any]]:
        """
        Executes a read-only query with performance monitoring.
        
        Args:
            query: SQL query string
            parameters: Query parameters dictionary
        
        Returns:
            List[Dict[str, Any]]: Query results as list of dictionaries
        """
        start_time = time.time()  # Initialize performance timer

        caller = inspect.currentframe().f_back.f_code.co_name

        try:

            with self.transaction() as session:

                log_prefix = f"[{caller}]"
                logger.info("%s - Executing read query", log_prefix)

                result = session.execute(text(query), parameters or {})
                columns = result.keys()
                data = []
                for row in result:
                    row_dict = dict(zip(columns, row))
                    data.append(row_dict)

                # Record execution metrics
                execution_time = time.time() - start_time
                logger.info("%s - Executed read query in %.2fs", log_prefix, execution_time)

                return data

        except Exception as e:

            execution_time = time.time() - start_time
            logger.error("Read query failed after %.2fs: %s", execution_time, e)
            raise


    def execute_write_query(self, query: str, parameters: dict = None) -> None:
        """
        Executes a write query within a transaction context.
        
        Args:
            query: SQL query string
            parameters: Query parameters dictionary
        """
        start_time = time.time()  # Initialize performance timer

        try:

            with self.transaction() as session:
                session.execute(text(query), parameters or {})

                # Record execution metrics
                execution_time = time.time() - start_time
                logger.info("Write query executed in %.2fs", execution_time)

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error("Write query failed after %.2fs: %s", execution_time, e)
            raise
