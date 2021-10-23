import logging


def Logger(name="LOG", level=logging.INFO):
    # logger = logging.getLogger(name)
    # logger.setLevel(level)
    # file_handler = logging.FileHandler('../logs/log_data.log')
    # formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s][%(message)s]')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)
    logging.basicConfig(format='[%(asctime)s][%(levelname)s]%(message)s', level=level, datefmt='%m/%d/%Y %H:%M:%S')
    return logging
