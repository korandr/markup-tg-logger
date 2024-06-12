import logging


MAX_MESSAGE_LENGTH = 4096

URL = 'https://api.telegram.org/bot{bot_token}/sendMessage'

HTML_CODE_TEMPLATE = '<pre><code class="language-python">{text}</code></pre>'

DEFAULT_LEVEL_NAMES = {
        logging.DEBUG:    '⬛️ DEBUG ⬛️',
        logging.INFO:     '⬜️ INFO ⬜️',
        logging.WARNING:  '🟨 WARNING 🟨',
        logging.ERROR:    '🟥 ERROR 🟥',
        logging.CRITICAL: '🟪 CRITICAL 🟪',
    }


