from collections.abc import Callable
from types import TracebackType
from typing import TypeAlias, Literal


EscapeFunc: TypeAlias = Callable[[str], str]
FormatStyle: TypeAlias = Literal['%', '{', '$']
LogLevel: TypeAlias = int | str
ParseMode: TypeAlias = Literal['', 'HTML', 'Markdown', 'MarkdownV2']
SysExcInfoType: TypeAlias = tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None]
