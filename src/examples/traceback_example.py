import logging

from markup_tg_logger import HtmlTracebackTelegramFormatter, BaseTelegramHandler

from config import BOT_TOKEN, CHAT_ID


formatter = HtmlTracebackTelegramFormatter(
    fmt = '<b>{levelname}</b>\n{asctime}\n\n{message}',
    datefmt = '%d-%m-%Y %H:%M:%S',
    style = '{',
    is_escape_markup = True
)

handler = BaseTelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
)

handler.setLevel(logging.ERROR)
handler.setFormatter(formatter)

logger = logging.getLogger('markup_tg_logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

try:
    raise ValueError('Error <description>')
except Exception as e:
    logger.exception(e)
