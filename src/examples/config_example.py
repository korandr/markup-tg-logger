import logging
from logging.config import dictConfigClass
import os

import markup_tg_logger


CONFIG = {
    'version': 1,
    'formatters': {
        'telegram': {
            '()': markup_tg_logger.HtmlFormatter,
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'fmt': '<b>{levelname}</b>\n{asctime}\n\n<code>{message}</code>\n\n{pathname}:{lineno}',
            'style': '{',
        },
    },
    'handlers': {
        'telegram': {
            '()': markup_tg_logger.TelegramHandler,
            'level': 'DEBUG',
            'formatter': 'telegram',
            'bot_token': os.environ['BOT_TOKEN'],
            'chat_id': os.environ['CHAT_ID'],
            'disable_notification': markup_tg_logger.LevelNotifier(logging.ERROR),
        },
    },
    'loggers': {
        'example': {},
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['telegram'],
    },
}

dict_config = dictConfigClass(CONFIG)
dict_config.configure()
logger = logging.getLogger('example')

logger.info('Hello HTML world!\nAny special characters: > < &')

