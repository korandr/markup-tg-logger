import logging
import os

from markup_tg_logger import TelegramHandler, HtmlFormatter


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = int(os.environ["CHAT_ID"])

formatter = HtmlFormatter(
    fmt = '<b>{levelname}</b>\n\n{message}',
    style = '{',
    escape_message = False,
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

logger.info('Hello <u>HTML</u> world!\nAny <b>special</b> characters: &gt; &lt; &amp;')
