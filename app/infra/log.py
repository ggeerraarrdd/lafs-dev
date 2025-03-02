"""
TD
"""

import logging
import os











def setup_logging():
    """
    TD
    """
    # Configure logging without file output initially
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        # Get the project root directory (parent of 'app' directory)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        log_dir = os.path.join(root_dir, 'logs')

        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)

        # Add file handler after directory is created
        file_handler = logging.FileHandler(os.path.join(log_dir, 'database_manager.log'))
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        # Get root logger and add file handler
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)

    except Exception as e: # pylint: disable=broad-exception-caught
        logging.warning("Could not set up file logging: %s", e)
        # Continue with console logging only
