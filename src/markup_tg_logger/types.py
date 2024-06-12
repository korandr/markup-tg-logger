from typing import TypeAlias, Literal
from types import TracebackType

ParseMode: TypeAlias = Literal['', 'HTML', 'MarkdownV2', 'Markdown']
LoggerLevel: TypeAlias = int | str
FormatStyle: TypeAlias = Literal["%", "{", "$"]
SysExcInfoType: TypeAlias = tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None]
