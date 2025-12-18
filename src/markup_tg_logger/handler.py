from importlib.util import find_spec
from logging import Handler, LogRecord
from typing import Any, override

from .exceptions import SenderError
from .formatters import BaseMarkupFormatter
from .interfaces import INotifier, ITelegramSender
from .interfaces import ITelegramSender
from .message_splitters.factory import MessageSplitterFactory, ParseModeToSplitter
from .notifiers import StaticNotifier
from .resolve_object_from_config import resolve_object_from_config
from .types import ParseMode

DefaultTelegramSender: type[ITelegramSender]

if find_spec('requests') is None:
    from .telegram_senders.http_client import HttpClientTelegramSender
    DefaultTelegramSender = HttpClientTelegramSender
else:
    from .telegram_senders.requests import RequestsTelegramSender 
    DefaultTelegramSender = RequestsTelegramSender


class TelegramHandler(Handler):
    """Logger handler that sends messages via a bot to Telegram.

    - Allows you to send logs to multiple chats at once.
    - When set as a formatter to `BaseMarkupFormatter` and derived classes, allows you to use
    Telegram-supported markup languages.
    - Splits overly long log entries into multiple messages that do not exceed the character limit,
    using `IMessageSplitter` implementations.
    - Allows you to customize message notifications using `INotifier` implementations.
    
    Docs:
        Handler: https://docs.python.org/3/library/logging.html#logging.Handler
    """

    def __init__(
        self,
        bot_token: str,
        chat_id: int | str | set[int | str] | list[int | str],
        disable_notification: bool | dict[str, Any] | INotifier = False,
        message_splitter_factory: MessageSplitterFactory | ParseModeToSplitter | None = None,
        sender: ITelegramSender | dict[str, Any] = DefaultTelegramSender(),
        force_send_on_exception: bool = False,
        **params: Any
    ) -> None:
        """
        Args:
            bot_token: Telegram bot API token.
            chat_id: Unique identifier for the target chat or username of the target channel (in
                the format `@channelusername`) or list/set for multiple recipients. 
            disable_notification: Customize notifications. In case of bool values, notifications
                will be always on or off. For more flexible customization, use `INotifier`
                implementations. A dictionary can be specified to support configuration from a file.
            message_splitter_factory: Factory for creating splitters depending on the markup 
                language or a dictionary with `ParseMode` to `IMessageSplitter` mappings that
                will be passed to the constructor of the `MessageSplitterFactory`. See the
                `MessageSplitterFactory` constructor documentation for details.
            sender: Telegram Bot API adapter that sends messages to Telegram. A dictionary can be
                specified to support configuration from a file.
            force_send_on_exception: If `True`, in case the handler sends a message to multiple
                recipients and an exception occurs during the process, the handler will forcefully
                continue sending messages to the remaining recipients. By default, if an exception
                occurs, the mailing is interrupted.
            **params: Other parameters of the Telegram Bot API `sendMessage` method.

        Initialization from the configuration dictionary:
            Arguments `disable_notification` and `sender` support the configuration dictionary
            format. The dictionary must contain the `'()'` key with the import path for the
            requested class as a string. The remaining dictionary keys will be passed to the
            constructor of the specified class.   
            
            Example with a sender: 
            ```python
            sender = {
                '()': 'markup_tg_logger.telegram_senders.http_client.HttpClientTelegramSender'
            }
            ```

            Example with a notifier:
            ```python
            disable_notification = {
                '()': 'markup_tg_logger.notifiers.level.LevelNotifier',
                'level': 'WARNING',
            }
            ```

            You can also pass your custom classes in the same way.
        """

        super().__init__()
        
        self._bot_token = bot_token
        self._chat_ids: set[int | str]
        self._notifier: INotifier
        self._message_splitter_factory: MessageSplitterFactory
        self._sender: ITelegramSender
        self._force_send_on_exception = force_send_on_exception
        self._params = params

        if isinstance(chat_id, (int, str)):
            self._chat_ids = {chat_id, }
        elif isinstance(chat_id, list):
            self._chat_ids = set(chat_id)
        else:
            self._chat_ids = chat_id

        if isinstance(disable_notification, bool):
            self._notifier = StaticNotifier(disable_notification)
        elif isinstance(disable_notification, dict):
            self._notifier = resolve_object_from_config(
                disable_notification,
                INotifier, # type: ignore[type-abstract] 
                           # https://github.com/python/mypy/issues/4717
            )
        else:
            self._notifier = disable_notification

        if isinstance(sender, dict):
            self._sender = resolve_object_from_config(
                sender,
                ITelegramSender, # type: ignore[type-abstract]
                                 # https://github.com/python/mypy/issues/4717
            )
        else:
            self._sender = sender

        if message_splitter_factory is None:
            self._message_splitter_factory = MessageSplitterFactory()
        elif isinstance(message_splitter_factory, dict):
            self._message_splitter_factory = MessageSplitterFactory(message_splitter_factory)
        else:
            self._message_splitter_factory = message_splitter_factory

    @override
    def emit(self, record: LogRecord) -> None:
        """Format log record, split to messages and send to Telegram."""

        text = self.format(record)

        parse_mode = self._get_parse_mode()
        splitter = self._message_splitter_factory.get(parse_mode)
        messages = splitter.split(text)

        disable_notification = self._notifier.disable_notification(record)

        try:
            for message in messages:
                try:
                    for chat_id in self._chat_ids:
                        try:
                            self._sender.send(
                                bot_token = self._bot_token,
                                chat_id = chat_id,
                                text = message,
                                parse_mode = parse_mode,
                                disable_notification = disable_notification,
                                **self._params
                            )
                        except SenderError:
                            if not self._force_send_on_exception: raise
                except SenderError:
                    if not self._force_send_on_exception: raise

        except SenderError:
            self.handleError(record)
        
    def _get_parse_mode(self) -> ParseMode:
        """Extract parse mode from formatter.
        
        If the formatter is not associated with `BaseMarkupFormatter`,
        then parse mode is not applied.
        """

        parse_mode: ParseMode = ''
        if isinstance(self.formatter, BaseMarkupFormatter):
            parse_mode = self.formatter.parse_mode

        return parse_mode
