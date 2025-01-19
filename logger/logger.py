import logging
import sys

class CustomLogger:
    """
    A custom logger class to handle logging for both FastAPI and FacebookClient.
    """

    def __init__(self, name: str = "app_logger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create console handler with a formatter
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        self.logger.addHandler(console_handler)

    def info(self, msg: str):
        """Log INFO level messages"""
        self.logger.info(msg)

    def debug(self, msg: str):
        """Log DEBUG level messages"""
        self.logger.debug(msg)

    def error(self, msg: str):
        """Log ERROR level messages"""
        self.logger.error(msg)

    def exception(self, msg: str):
        """Log exception messages"""
        self.logger.exception(msg)

    def warn(self, msg: str):
        """Log WARNING level messages"""
        self.logger.warning(msg)