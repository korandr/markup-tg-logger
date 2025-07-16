import logging
import os
import time

from markup_tg_logger import BaseMarkupFormatter, TelegramHandler, LevelNotifier


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = int(os.environ["CHAT_ID"])

formatter = BaseMarkupFormatter(
    fmt = '{levelname}\n{asctime}\n\n{message}',
    datefmt = '%d-%m-%Y %H:%M:%S',
    style = '{'
)

handler = TelegramHandler(
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
