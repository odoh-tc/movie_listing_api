import logging
import sys
from logging.handlers import SysLogHandler
from app.core.config import settings

# Initialize logger
logger = logging.getLogger("movie_listing_app")
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(filename)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Stream handler (logs to terminal)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# SysLog handler (logs to Papertrail)
syslog_handler = SysLogHandler(address=(settings.PAPERTRAIL_URL, settings.PAPERTRAIL_PORT))
syslog_handler.setFormatter(formatter)

# Add handlers to logger
logger.handlers = [stream_handler, syslog_handler]
logger.setLevel(logging.DEBUG)
