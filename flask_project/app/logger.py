"""
The module in which the logger for the web project is implemented
"""
from logging import Handler

from loguru import logger


class InterceptHandler(Handler):
    """
    The class extends the work of the standard logger.
    """

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


logger.add('logs/error.json', level="ERROR", format="{time} {level}: '{message}'",
           rotation="00:00", compression="zip", serialize=True)

logger.add('logs/info.json', level="INFO", format="{time} {level}: '{message}'",
           rotation="00:00", compression="zip", serialize=True)
