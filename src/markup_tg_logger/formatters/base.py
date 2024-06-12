from typing import List
from logging import Formatter, LogRecord

from ..config import DEFAULT_LEVEL_NAMES, MAX_MESSAGE_LENGTH
from ..types import ParseMode, FormatStyle
from ..interfaces import IMessageSplitter
from ..message_splitters import BaseMessageSplitter


class BaseTelegramFormatter(Formatter):
    def __init__(
            self,
            fmt: str,
            datefmt: str = None,
            style: FormatStyle = '%',
        ) -> None:
        
        super().__init__(fmt, datefmt, style)

        self._MAX_MESSAGE_LENGTH = MAX_MESSAGE_LENGTH
        self._level_names = DEFAULT_LEVEL_NAMES
        self._splitter: IMessageSplitter = BaseMessageSplitter()

    @property
    def parse_mode(self) -> ParseMode:
        return self._splitter.parse_mode

    def format(self, record: LogRecord) -> List[str]:
        self._prepare_record(record)
        text = super().format(record)
        
        return self._splitter.split(text)

    def _prepare_record(self, record: LogRecord) -> None:
        self._replace_level_names(record)

    def _replace_level_names(self, record: LogRecord) -> None:
        if record.levelno in self._level_names.keys():
            record.levelname = self._level_names[record.levelno]

