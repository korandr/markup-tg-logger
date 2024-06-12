import time
import logging

from markup_tg_logger import BaseTelegramFormatter, BaseTelegramHandler, LevelNotifier

from config import BOT_TOKEN, CHAT_ID


formatter = BaseTelegramFormatter(
    fmt = '{levelname}\n{asctime}\n\n{message}',
    datefmt = '%d-%m-%Y %H:%M:%S',
    style = '{'
)

handler = BaseTelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
    disable_notification = LevelNotifier(logging.ERROR)
)

handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger('markup_tg_logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('Message without notification')
time.sleep(5)
logger.critical('Important notification message')

