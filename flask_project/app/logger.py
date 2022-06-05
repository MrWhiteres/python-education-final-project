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


logger.level("login_User", no=25, color="<blue><bold>", icon='-_-')
logger.level("New_User", no=30, color="<white><bold>", icon='@')
logger.level("New_Film", no=35, color="<white><bold>", icon="$")
logger.level("Show", no=40, color="<green><bold>", icon='+_+')
logger.level("Del_Film", no=50, color="<yellow><bold>", icon='/!\\')
logger.level("Edit_Film", no=55, color="<red><bold>", icon='/!\\')
logger.level("Error", no=45, color='<red><bold>', icon='❌')

logger.add('logs/show.json', level="Show", format="{time} {level}: '{message}'",
           rotation="00:00", compression="zip", serialize=True)

logger.add('logs/login_user.json', level="login_User", format="{time} {level}: '{message}'",
           rotation="00:00", compression="zip", serialize=True)

logger.add('logs/new_user.json', level="New_User", format="{time} {level}: '{message}'",
           rotation="00:00", compression="zip", serialize=True)

logger.add('logs/new_film.json', level="New_Film", format="{time} {level}: '{message}'",
           rotation="00:00", compression="zip", serialize=True)

logger.add('logs/del_film.json', level="Del_Film", format="{time} {level}: '{message}'",
           rotation="00:00", compression="zip", serialize=True)

logger.add('logs/errors.json', level="Error", format="{time} {level}: '{message}'",
           rotation="00:00", compression="zip", serialize=True)

logger.add('logs/edit_film.json', level="Edit_Film", format="{time} {level}: '{message}'",
           rotation="00:00", compression="zip", serialize=True)
