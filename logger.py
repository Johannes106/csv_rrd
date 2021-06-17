import logging


class Logger:
    # With the __new__ function the Logger is converted to a singleton
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not Logger.__instance:
            Logger.__instance = object.__new__(cls)
        return Logger.__instance


    def __init__(self, name):
        self.name = name
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%d.%m.%Y %I:%M:%S %p', filename=name, level=logging.DEBUG)

    def i(self, text):
        logging.info(text)

    def w(self, text):
        logging.warning(text)
