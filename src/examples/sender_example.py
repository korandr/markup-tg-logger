import logging
import os

from markup_tg_logger import TelegramHandler
from markup_tg_logger.telegram_senders.http_client import HttpClientTelegramSender
from markup_tg_logger.telegram_senders.requests import RequestsTelegramSender


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = int(os.environ["CHAT_ID"])

formatter = logging.Formatter(fmt='[{name}]: {message}', style='{')

handler = TelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
    sender = HttpClientTelegramSender(),
)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

http_client_logger = logging.getLogger('http.client')
http_client_logger.setLevel(logging.DEBUG)
http_client_logger.addHandler(handler)


handler = TelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
    sender = RequestsTelegramSender(),
)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

requests_logger = logging.getLogger('requests')
requests_logger.setLevel(logging.DEBUG)
requests_logger.addHandler(handler)
requests_logger.addHandler(handler)

http_client_logger.info('This message was sent via http.client')
requests_logger.info('This message was sent via requests')
