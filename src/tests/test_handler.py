"""Test the `TelegramHandler`."""

import logging
from logging import LogRecord
from typing import Any, override

from markup_tg_logger.formatters.base import BaseMarkupFormatter
from markup_tg_logger.handler import TelegramHandler
from markup_tg_logger.interfaces import IMessageSplitter, ITelegramSender, INotifier
from markup_tg_logger.message_splitters.factory import MessageSplitterFactory
from markup_tg_logger.types import ParseMode


SOURCE_TEXT = 'source text'
FORMATTED_TEXT = 'formatted text'
SPLITTED_TEXT = ['splitted text part 1', 'splitted text text part 2']
PARSE_MODE = 'HTML'
LEVEL = logging.INFO
DISABLE_NOTIFICATION = True
BOT_TOKEN = 'test-bot-token'
CHAT_ID = 'test-chat-id'


class FakeMessageSplitter(IMessageSplitter):
    @property
    @override
    def parse_mode(self) -> ParseMode:
        return PARSE_MODE

    @override
    def split(self, text: str) -> list[str]:
        assert text == FORMATTED_TEXT

        return SPLITTED_TEXT


class FakeMessageSplitterFactory(MessageSplitterFactory):
    @override
    def get(self, parse_mode: ParseMode) -> IMessageSplitter:
        assert parse_mode == PARSE_MODE

        return FakeMessageSplitter() 


class FakeNotifier(INotifier):
    @override
    def disable_notification(self, record: logging.LogRecord) -> bool:
        assert record.levelno == LEVEL

        return DISABLE_NOTIFICATION

class FakeFormatter(BaseMarkupFormatter):
    @override
    def __init__(self) -> None:
        pass

    @property
    @override
    def parse_mode(self) -> ParseMode:
        return PARSE_MODE

    @override
    def format(self, record: LogRecord) -> str:
        assert record.msg == SOURCE_TEXT

        return FORMATTED_TEXT


class FakeSender(ITelegramSender):
    def __init__(self) -> None:
        self.received_data: dict = {}

    @override
    def send(
        self,
        bot_token: str,
        chat_id: int | str,
        text: str,
        parse_mode: str = '',
        disable_notification: bool = False,
        **params: dict[str, Any]
    ) -> None:
        self.received_data = {
            'bot_token': bot_token, 
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
            **params,
        }
        

def test_emit() -> None:
    sender = FakeSender()

    handler = TelegramHandler(
        bot_token = BOT_TOKEN,
        chat_id = CHAT_ID,
        disable_notification = FakeNotifier(),
        message_splitter_factory = FakeMessageSplitterFactory(),
        sender = sender,
    )

    handler.setFormatter(FakeFormatter())
    
    record = logging.makeLogRecord({
        'name': 'test_logger',
        'levelno': logging.INFO,
        'levelname': logging._levelToName[logging.INFO],
        'msg': SOURCE_TEXT,
    })

    handler.emit(record)

    data = sender.received_data

    assert data['bot_token'] == BOT_TOKEN
    assert data['chat_id'] == CHAT_ID
    assert data['text'] == SPLITTED_TEXT[1]
    assert data['parse_mode'] == PARSE_MODE
    assert data['disable_notification'] == DISABLE_NOTIFICATION
