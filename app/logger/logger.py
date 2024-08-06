import logging
import sys

logger = logging.getLogger("myapp")
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(filename)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.handlers = [stream_handler]
logger.setLevel(logging.DEBUG)
