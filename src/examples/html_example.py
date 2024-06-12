import logging

from markup_tg_logger import HtmlTelegramFormatter, BaseTelegramHandler

from config import BOT_TOKEN, CHAT_ID


FORMAT = '''<b>{levelname}</b>

<u>{asctime}</u>

<i>{message}</i>

<pre><code class="language-bash">(Line: {lineno} [{pathname}])</code></pre>
'''

formatter = HtmlTelegramFormatter(
    fmt = FORMAT,
    datefmt = '%d-%m-%Y %H:%M:%S',
    style = '{',
    is_escape_markup = True
)

handler = BaseTelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
)

handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger('markup_tg_logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('Hello HTML world! \n Any special characters: ><& <3')

