import logging

logging.basicConfig(level=logging.INFO)

def log_info(msg: str):
    logging.info(msg)

def log_error(msg: str):
    logging.error(msg)
