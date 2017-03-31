import logging
from enum import IntEnum


class Logger(object):
    __logger = None

    class Level(IntEnum):
        CRITICAL = 50
        ERROR = 40
        WARNING = 30
        INFO = 20
        DEBUG = 10
        NOTSET = 0

    class _Logger(object):
        def __init__(self,
                     filename_output=None,
                     console_output=True,
                     gobal_level=None,
                     global_format="%(levelname)s:%(name)s:%(message)s"
                     ):
            """
            
            :param filename_output: 
            :param console_output: 
            :param gobal_level: 
            :param global_format: 
            """

            self._loggers = dict()
            self.formatter = logging.Formatter(global_format)
            self._global_level = gobal_level

            root = self.get_logger()

            if console_output:
                handler = logging.StreamHandler()
                handler.setFormatter(self.formatter)
                root.addHandler(handler)
            if filename_output:
                handler = logging.FileHandler(filename_output)
                handler.setFormatter(self.formatter)
                root.addHandler(handler)

        @property
        def global_level(self):
            return self._global_level

        @global_level.setter
        def global_level(self, value):
            for i in self._loggers.values():
                i.setLevel(value)

        def get_logger(self, name=None):
            """

              :param name:             
              :return: 
              :rtype: logging.Logger
             """
            new_logger = None
            if name not in self._loggers:
                if name:
                    self._loggers[name] = new_logger = logging.getLogger(name)
                else:
                    self._loggers[name] = new_logger = logging.getLogger()
            if new_logger and self.global_level is not None:
                new_logger.setLevel(self.global_level)

            return self._loggers[name]

    def __init__(self, *args, **kwargs):
        """

        :param filename_output: 
        :param console_output: 
        :param gobal_level: 
        :param global_format: 
        """
        if Logger.__logger is None:
            Logger.__logger = Logger._Logger(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(Logger.__logger, item)

    def __setattr__(self, key, value):
        setattr(Logger.__logger, key, value)
