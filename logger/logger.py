import logging


logging.basicConfig(
    filename='logger/logfile.txt',
    filemode='a',
    format='%(asctime)s %(levelname)s-%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_warning(message):
    logging.warning(message)


def log_critical(message):
    logging.critical(message)


def log_error(message):
    logging.critical(message)
