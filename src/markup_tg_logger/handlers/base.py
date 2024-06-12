from typing import Dict, Any, List
from logging import Handler, LogRecord

from requests.exceptions import RequestException

from ..interfaces import INotifier
from ..telegram import TelegramSender
from ..notifiers import StaticNotifier
from ..message_splitters import BaseMessageSplitter
from ..formatters import BaseTelegramFormatter


class BaseTelegramHandler(Handler):
    def __init__(
            self,
            bot_token: str,
            chat_id: int | str,
            disable_notification: bool | INotifier = False,
            **params: Dict[str, Any]
        ):
        super().__init__()
        
        self._bot_token = bot_token
        self._chat_id = chat_id
        self._params = params

        self._sender = TelegramSender()
        self._notifier: INotifier = StaticNotifier(disable_notification) if isinstance(disable_notification, bool) else disable_notification

    def emit(self, record:LogRecord) -> None:
        if isinstance(self.formatter, BaseTelegramFormatter):
            messages = self.format(record)
            parse_mode = self.formatter.parse_mode
        else:
            text = self.format(record)
            splitter = BaseMessageSplitter()
            messages = splitter.split(text)
            parse_mode = splitter.parse_mode

        disable_notification = self._notifier.is_disable_notification(record)

        try:
            for message in messages:
                self._sender.send(self._bot_token, self._chat_id, message, parse_mode, disable_notification, **self._params)

        except RequestException:
            self.handleError(record)
        
