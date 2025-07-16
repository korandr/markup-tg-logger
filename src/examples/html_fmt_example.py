import logging
import os

from markup_tg_logger import TelegramHandler, HtmlFormatter


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = int(os.environ["CHAT_ID"])

FMT = (
    '<b>{levelname}</b>\n\n'
    '<u>{asctime}</u>\n\n'
    '<i>{message}</i>\n\n'
    '(Line: {lineno} [<code>{pathname}</code>])'
)

formatter = HtmlFormatter(
    fmt = FMT,
    datefmt = '%d-%m-%Y %H:%M:%S',
    style = '{',
)

handler = TelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger = logging.getLogger('example')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('Hello HTML world!\nAny special characters: > < &')
