"""
    ----------------------------------------------------------
    Copyright (C) 2023 Justin Kasteleijn - All Rights Reserved
    You may use, distribute and modify this code as it is
    open source
    ----------------------------------------------------------
"""

import logging
import functools
from typing import Dict, TypeVar, Callable, Type
from logging import config

T = TypeVar('T', bound='Logger')


def log(level=logging.DEBUG, log_args=False, log_kwargs=False, log_return=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            class_name: str = func.__qualname__[:func.__qualname__.index('.')]
            func_name: str = func.__name__
            logger: T = Logger()
            if log_args and log_kwargs:
                logger.log(level, f"Function {class_name}.{func_name} called with args {args} and kwargs {kwargs}")
            elif log_args:
                logger.log(level, f"Function {class_name}.{func_name} called with args {args}")
            elif log_kwargs:
                logger.log(level, f"Function {class_name}.{func_name} called with kwargs {kwargs}")
            else:
                logger.log(level, f"Function {class_name}.{func_name} called")
            try:
                result = func(*args, **kwargs)
                if log_return:
                    logger.log(level, f"Function {class_name}.{func_name} returned {result}")
                else:
                    logger.log(level, f"Function {class_name}.{func_name} returned successfully")
                return result
            except Exception as e:
                logger.error(f"Function {class_name}.{func_name} raised an exception: {e}")
                raise

        return wrapper

    return decorator


class Logger:
    _instance: T = None
    _logger: logging.Logger

    def __new__(cls: Type[T], *args, **kwargs) -> T:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            config.fileConfig('C:/Users/justi/nosnutri/front-end/Logger/logger.conf')
            cls._instance._logger = logging.getLogger(__name__)
        return cls._instance

    @classmethod
    def debug(cls: Type[T], message: str) -> None:
        cls.__set_level(logging.DEBUG)
        cls.__get_instance()._logger.debug(message)

    @classmethod
    def info(cls: Type[T], message: str) -> None:
        cls.__set_level(logging.INFO)
        cls.__get_instance()._logger.info(message)

    @classmethod
    def warning(cls: Type[T], message: str) -> None:
        cls.__set_level(logging.WARNING)
        cls.__get_instance()._logger.warning(message)

    @classmethod
    def error(cls: Type[T], message: str) -> None:
        cls.__set_level(logging.ERROR)
        cls.__get_instance()._logger.error(message)

    @classmethod
    def critical(cls: Type[T], message: str) -> None:
        cls.__set_level(logging.CRITICAL)
        cls.__get_instance()._logger.critical(message)

    @classmethod
    def log(cls: Type[T], level: int, message: str) -> None:
        logging_methods: Dict[int, Callable[[str], None]] = {
            logging.DEBUG: cls.debug,
            logging.INFO: cls.info,
            logging.WARNING: cls.warning,
            logging.ERROR: cls.error,
            logging.CRITICAL: cls.critical,
        }
        logging_methods[level](message)

    @classmethod
    def __set_level(cls: Type[T], level: int) -> None:
        cls.__get_instance()._logger.setLevel(level)

    @classmethod
    def __get_instance(cls: Type[T]) -> T:
        if not cls._instance:
            cls._instance = Logger()
        return cls._instance
