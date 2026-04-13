"""Test the `RequestsTelegramSender`."""

import pytest

from ..test_utils.telegram_server import (
    BAD_REQUEST_ENDPOINT,
    BOT_TOKEN,
    HOST,
    JsonHub,
    PORT,
    SAVE_JSON_ENDPOINT,
)

from markup_tg_logger.exceptions import SenderError
from markup_tg_logger.telegram_senders.requests import RequestsTelegramSender


CHAT_ID = 123
TEXT = 'test message'
PARSE_MODE = 'HTML'

@pytest.mark.unit()
def test_json(telegram_server_json_hub: JsonHub) -> None:
    telegram_server_json_hub.reset_saved_json()

    sender = RequestsTelegramSender(base_url=f'http://{HOST}:{PORT}', method=SAVE_JSON_ENDPOINT)

    sender.send(
        bot_token = BOT_TOKEN,
        chat_id = CHAT_ID,
        text = TEXT,
        parse_mode = PARSE_MODE,
    )

    data = telegram_server_json_hub.get_last_received_json()

    assert data is not None
    assert data['chat_id'] == CHAT_ID
    assert data['text'] == TEXT
    assert data['parse_mode'] == PARSE_MODE

@pytest.mark.unit()
def test_bad_request() -> None:
    sender = RequestsTelegramSender(base_url=f'http://{HOST}:{PORT}', method=BAD_REQUEST_ENDPOINT)

    with pytest.raises(SenderError):
        sender.send(
            bot_token = BOT_TOKEN,
            chat_id = CHAT_ID,
            text = TEXT,
        )

@pytest.mark.unit()
def test_http_error() -> None:
    sender = RequestsTelegramSender(
        base_url = f'http://{HOST}:{PORT}',
        method = 'wrong-endpoint-for-http-error',
    )

    with pytest.raises(SenderError):
        sender.send(
            bot_token = BOT_TOKEN,
            chat_id = CHAT_ID,
            text = TEXT,
        )
