from typing import override
from logging import LogRecord
from html import escape

from ..types import FormatStyle, SysExcInfoType
from ..message_splitters import HtmlMessageSplitter
from .base import BaseTelegramFormatter
    

class HtmlTelegramFormatter(BaseTelegramFormatter):
    @override
    def __init__(
            self,
            fmt: str,
            datefmt: str = None,
            style: FormatStyle = '%',
            is_escape_markup: bool = True,
        ) -> None:

        super().__init__(fmt, datefmt, style)

        self._is_escape_markup = is_escape_markup
        self._splitter = HtmlMessageSplitter()

    @override
    def _prepare_record(self, record: LogRecord) -> None:
        if record.getMessage() and self._is_escape_markup:
            record.msg = escape(record.getMessage(), quote=False)
            
        super()._prepare_record(record)
    
    @override
    def formatException(self, ei: SysExcInfoType) -> str:
        return escape(super().formatException(ei), quote=False)
    
    @override
    def formatStack(self, stack_info: str) -> str:
        return escape(super().formatStack(stack_info), quote=False)

