import logging
import os

from markup_tg_logger import TelegramHandler


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = int(os.environ["CHAT_ID"])

handler = TelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
)
handler.setLevel(logging.INFO)

logger = logging.getLogger('example')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('This message was sent via markup-tg-logger')
