import html
import logging
import pytest

from ..test_utils.telegram_server import HOST, PORT, JsonHub, SAVE_JSON_ENDPOINT

from markup_tg_logger.formatters.html import HtmlFormatter
from markup_tg_logger.handler import TelegramHandler
from markup_tg_logger.message_splitters.factory import MessageSplitterFactory
from markup_tg_logger.message_splitters.html import HtmlMessageSplitter
from markup_tg_logger.notifiers import LevelNotifier
from markup_tg_logger.telegram_senders.requests import RequestsTelegramSender


@pytest.mark.integration()
def test_usecase(telegram_server_json_hub: JsonHub) -> None:
    CHAT_ID = 12345
    TEXT = 'test text and << special chars >>'
    ESCAPED_TEXT = 'test text and &lt;&lt; special chars &gt;&gt;'
    LEVEL_NAME = 'LEVEL NAME'
    OPTIONAL_VALUE = 'optional_value'

    formatter = HtmlFormatter(
        fmt = '<b>{levelname}</b> {message}',
        style = '{',
        level_names = {logging.CRITICAL: LEVEL_NAME},
        escape_func = lambda text: html.escape(text, quote=False),
        escape_message = True,
        escape_result = False,
        result_template = '<result>{text}</result>',
    )

    sender = RequestsTelegramSender(url = f'http://{HOST}:{PORT}' + '/{bot_token}')

    splitter_factory = MessageSplitterFactory(
        parse_mode_to_splitter = {'HTML': HtmlMessageSplitter()}
    )

    handler = TelegramHandler(
        bot_token = SAVE_JSON_ENDPOINT,
        chat_id = CHAT_ID,
        disable_notification = LevelNotifier(logging.WARNING),
        message_splitter_factory = splitter_factory,
        sender = sender,
        optional_param = OPTIONAL_VALUE,
    )

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger = logging.getLogger('integration_test_logger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    logger.critical(TEXT)
    json = telegram_server_json_hub.get_last_received_json()

    assert json is not None
    assert json['chat_id'] == CHAT_ID
    assert json['text'] == f'<result><b>{LEVEL_NAME}</b> {ESCAPED_TEXT}</result>'
    assert json['disable_notification'] == False
    assert json['parse_mode'] == 'HTML'
    assert json['optional_param'] == OPTIONAL_VALUE
