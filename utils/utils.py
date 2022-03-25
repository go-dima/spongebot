import logging
from logging.handlers import RotatingFileHandler


def setup_logger(logger: logging.Logger):
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(level=logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    file_handler = RotatingFileHandler('logs/spongebot.log', maxBytes=1000000, backupCount=3)
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
