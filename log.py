import logging

from cloghandler import ConcurrentRotatingFileHandler

from settings import *

LOG_LEVEL = logging.getLevelName(LOG_LEVEL)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(message)s')

ROOT_LOG_NAME = ROOT_LOG_NAME

LOG_PATH = LOG_PATH

MAX_FILE_SIZE = 100 * 2 ** 20


def get_log_name(name):
    if name == ROOT_LOG_NAME:
        return ROOT_LOG_NAME

    return ''.join([ROOT_LOG_NAME, '.', name])


def get_handler(filename, level=None):
    ext = logging.getLevelName(level).lower() if level is not None else 'log'
    handler = ConcurrentRotatingFileHandler(''.join([LOG_PATH, filename, '.', ext]),
                                            mode='a',
                                            maxBytes=MAX_FILE_SIZE,
                                            backupCount=5,
                                            encoding='utf-8')
    handler.setFormatter(formatter)
    if level is not None:
        handler.setLevel(level)

    return handler


def get_root_logger():
    root_logger = get_logger(ROOT_LOG_NAME)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(LOG_LEVEL)
    root_logger.addHandler(stream_handler)
    return root_logger

logs = set()


def get_logger(name, filename=None):

    logger = logging.getLogger(get_log_name(name))

    if filename is None:
        filename = name

    if name not in logs:
        logger.setLevel(LOG_LEVEL)

        try:
            logger.addHandler(get_handler(filename))
            logger.addHandler(get_handler(filename, level=logging.ERROR))
        except IOError:
            return logger

        logs.add(name)

    return logger


logger = get_root_logger()

if __name__ == '__main__':
    test_log = get_logger("test")
    test_log.info('This is INFO LOG')
    test_log.debug('This is DEBUG LOG')
    test_log.error('This is ERROR LOG')
