from typing import override, List
from logging import LogRecord, Formatter
from html import escape

from ..types import FormatStyle
from ..config import HTML_CODE_TEMPLATE
from ..message_splitters import HtmlMessageSplitter
from .base import BaseTelegramFormatter
    

class CodeTelegramFormatter(BaseTelegramFormatter):
    @override
    def __init__(
            self,
            fmt: str,
            datefmt: str = None,
            style: FormatStyle = '%',
        ) -> None:

        super().__init__(fmt, datefmt, style)

        self._TEMPLATE = HTML_CODE_TEMPLATE
        self._splitter = HtmlMessageSplitter()
    
    @override
    def format(self, record: LogRecord) -> List[str]:
        self._prepare_record(record)
        text = Formatter.format(self, record)
        text = escape(text, quote=False)

        text = self._TEMPLATE.format(text=text)
        
        return self._splitter.split(text)

