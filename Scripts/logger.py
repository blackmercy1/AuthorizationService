import logging


class Logger:
    logger: logging.Logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler: logging.FileHandler = logging.FileHandler('app.log')
    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
