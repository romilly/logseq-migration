import logging


class LoggingMonitor:
    def __init__(self, debug_level: int):
        logging.basicConfig(level=logging.DEBUG,
                            filename='migration.log',
                            filemode='a')

    def print(self, message: str):
        logging.debug(message)
