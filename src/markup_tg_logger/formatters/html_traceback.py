from typing import override, List
from logging import LogRecord, Formatter
from html import escape

from ..types import FormatStyle, SysExcInfoType
from ..config import HTML_CODE_TEMPLATE
from .html import HtmlTelegramFormatter, BaseTelegramFormatter
    

class HtmlTracebackTelegramFormatter(HtmlTelegramFormatter):
    @override
    def __init__(
            self,
            fmt: str,
            datefmt: str = None,
            style: FormatStyle = '%',
            is_escape_markup: bool = True,
        ) -> None:

        super().__init__(fmt, datefmt, style, is_escape_markup)

        self._TEMPLATE = HTML_CODE_TEMPLATE
    
    @override
    def formatException(self, ei: SysExcInfoType) -> str:
        return self._TEMPLATE.format(text=super().formatException(ei))

    @override
    def formatStack(self, stack_info: str) -> str:
        return self._TEMPLATE.format(text=super().formatStack(stack_info))

