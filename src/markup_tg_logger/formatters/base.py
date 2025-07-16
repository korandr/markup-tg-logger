from collections.abc import Mapping
from logging import Formatter, LogRecord
from typing import override, Any

from ..defaults import DEFAULT_LEVEL_NAMES
from ..types import ParseMode, FormatStyle


class BaseMarkupFormatter(Formatter):
    """Base class of the library formatter.
    
    Defines the `parse_mode` property interface for interaction with `TelegramHandler`.

    The formatter behaves like the standard `logging.Formatter`, optionally replacing the
    displayedlevel names. It does not use escaping.

    To add escaping, create a derived class and override the methods `_pre_format` and
    `_post_format`. Also, if necessary, use the methods `formatMesage`, `formatException` and
    `formatStack`, which are inherited from `logging.Formatter`. Or use the derived classes
    included in the library.

    Docs:
        `logging.Formatter`: https://docs.python.org/3/library/logging.html#logging.Formatter.
    """

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: FormatStyle = '%',
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
        level_names: dict[int, str] = DEFAULT_LEVEL_NAMES,
        parse_mode: ParseMode = '',
    ) -> None:
        """
        Args:
            fmt: A format string in the given style for the logged output as a whole. The possible
                mapping keys are drawn from the `LogRecord` object's `LogRecord` attributes. If not
                specified, `%(message)s` is used, which is just the logged message.
            datefmt: A format string in the given style for the date/time portion of the logged
                output. If not specified, the default described in `formatTime()` is used.
            style: Can be one of `%`, `{` or `$` and determines how the format string will be
                merged with its data: using one of printf-style String Formatting (%),
                `str.format()` ({) or string.Template ($). This only applies to fmt and datefmt
                (e.g. `%(message)s` versus `{message}`), not to the actual log messages passed
                to the logging methods. However, there are other ways to use {- and $-formatting
                for log messages.
            validate:  If `True` (the default), incorrect or mismatched `fmt` and `style` will
                raise a `ValueError`; for example, `BaseMarkupFormatter('%(message)s', style='{')`.
            defaults:
                A dictionary with default values to use in custom fields. For example,
                `BaseMarkupFormatter('%(ip)s %(message)s', defaults={"ip": None})`.
            level_names: Mapping between numeric logging level IDs and their names. For example,
                `{30: 'WARN'}` or `{logging.WARNING: 'WARN'}`. By default, names will be appended
                with colored emoji. The dictionary does not have to override all level names.
                To use the default names, use `level_names = {}`.
            parse_mode: The markup language that Telegram needs to parse to display formatted text.
                Defaults to `''` (Plain Text).

        Docs:
            - Parameters `fmt`, `datefmt`, `style`, `validate`, `defaults` by `logging.Formatter`:
            https://docs.python.org/3/library/logging.html#logging.Formatter
            - Logging levels: https://docs.python.org/3/library/logging.html#logging-levels
            - Telegram Bot API formatting options: https://core.telegram.org/bots/api#formatting-options
        """
        
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

        self._level_names = level_names
        self._parse_mode: ParseMode = parse_mode

    @property
    def parse_mode(self) -> ParseMode:
        """The markup language that the formatter works with."""

        return self._parse_mode
    
    @override
    def format(self, record: LogRecord) -> str:
        self._pre_format(record)
        text = super().format(record)
        text = self._post_format(text)
        
        return text

    def _pre_format(self, record: LogRecord) -> None:
        """Prepare log entry for formatting.

        The method will be called before calling `logging.Formatter.format()`.
        By default, it only calls the `_replace_level_name()` method.

        Args:
            record: A log entry that requires formatting.
        """

        self._replace_level_name(record)

    def _post_format(self, text: str) -> str:
        """Additional operations with text after formatting.
        
        The method will be called after `logging.Formatter.format()` is called. Does nothing
        in this implementation. Designed to be overridden in derived classes.

        Args:
            text: Log entry text formatted using other methods.
        """

        return text

    def _replace_level_name(self, record: LogRecord) -> None:
        """Change the default logging level name.
        
        The name will remain unchanged unless an alternative name is specified in `_level_names`.
        """

        if record.levelno in self._level_names.keys():
            record.levelname = self._level_names[record.levelno]
