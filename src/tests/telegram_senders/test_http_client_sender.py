"""Test the `HttpClientTelegramSender`."""

from collections.abc import Generator
import pytest

from ..test_utils.telegram_server import (
    JsonHub, HOST, PORT, SAVE_JSON_ENDPOINT, BAD_REQUEST_ENDPOINT,
)

from markup_tg_logger.exceptions import SenderError
from markup_tg_logger.interfaces import ITelegramSender
from markup_tg_logger.telegram_senders.http_client import HttpClientTelegramSender


CHAT_ID = 123
TEXT = 'test message'
PARSE_MODE = 'HTML'

@pytest.fixture()
def sender() -> Generator[ITelegramSender, None, None]:
    sender = HttpClientTelegramSender(
        url = f'http://{HOST}:{PORT}' + '{bot_token}',
    )

    yield sender

@pytest.mark.unit()
def test_json(telegram_server_json_hub: JsonHub, sender: ITelegramSender) -> None:
    telegram_server_json_hub.reset_saved_json()

    sender.send(
        bot_token = SAVE_JSON_ENDPOINT,
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
def test_bad_request(sender: ITelegramSender) -> None:
    with pytest.raises(SenderError):
        sender.send(
            bot_token = BAD_REQUEST_ENDPOINT,
            chat_id = CHAT_ID,
            text = TEXT,
        )

@pytest.mark.unit()
def test_http_error(sender: ITelegramSender) -> None:
    with pytest.raises(SenderError):
        sender.send(
            bot_token = '/wrong-endpoint-for-http-error',
            chat_id = CHAT_ID,
            text = TEXT,
        )
