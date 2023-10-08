import logging

logging.basicConfig(level=logging.INFO)
logger_geneartor = lambda x: logging.getLogger(x)