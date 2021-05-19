import logging


class Logger:
    def __init__(self, name):
        self.name = name
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%d.%m.%Y %I:%M:%S %p', filename=name, level=logging.DEBUG)

    def i(self, text):
        logging.info(text)

    def w(self, text):
        logging.warning(text)
