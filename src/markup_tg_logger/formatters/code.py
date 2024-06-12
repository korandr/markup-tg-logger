from typing import override, List
from logging import LogRecord, Formatter
from html import escape

from ..types import FormatStyle
from ..config import HTML_CODE_TEMPLATE
from .html import HtmlTelegramFormatter
    

class CodeTelegramFormatter(HtmlTelegramFormatter):
    @override
    def __init__(
            self,
            fmt: str,
            datefmt: str = None,
            style: FormatStyle = '%',
        ) -> None:

        super().__init__(fmt, datefmt, style, is_escape_markup=True)

        self._TEMPLATE = HTML_CODE_TEMPLATE
    
    @override
    def format(self, record: LogRecord) -> List[str]:
        self._prepare_record(record)
        text = Formatter.format(self, record)

        text = self._TEMPLATE.format(text=text)
        
        return self._splitter.split(text)

