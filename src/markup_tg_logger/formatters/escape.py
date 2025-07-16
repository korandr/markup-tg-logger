from collections.abc import Mapping
from logging import LogRecord
from typing import override, Any

from ..defaults import DEFAULT_LEVEL_NAMES
from ..types import FormatStyle, SysExcInfoType, EscapeFunc, ParseMode
from .base import BaseMarkupFormatter
    

class EscapeMarkupFormatter(BaseMarkupFormatter):
    """A formatter for setting up the escaping of special characters of the selected markup language.

    Example for HTML:
    ```python
    import html

    formatter = EscapeMarkupFormatter(
        fmt = '<b>{levelname}</b> <u>{asctime}</u> <i>{message}</i> <code>{pathname}</code>',
        style = '{',
        parse_mode = 'HTML',
        escape_func = lambda text: html.escape(text, quote=False),
        stack_info_tamplate = '<code>{text}</code>',
        exception_template = '<code>{text}</code>',
    )
    ```
    """

    @override
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
        escape_func: EscapeFunc = lambda text: text,
        escape_message: bool = True,
        escape_stack_info: bool = True,
        escape_exception: bool = True,
        escape_result: bool = False,
        stack_info_template: str = '{text}',
        exception_template: str = '{text}',
        result_template: str = '{text}',
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
                raise a `ValueError`; for example, `EscapeMarkupFormatter('%(message)s', style='{')`.
            defaults:
                A dictionary with default values to use in custom fields. For example,
                `EscapeMarkupFormatter('%(ip)s %(message)s', defaults={"ip": None})`.
            level_names: Mapping between numeric logging level IDs and their names. For example,
                `{30: 'WARN'}` or `{logging.WARNING: 'WARN'}`. By default, names will be appended
                with colored emoji. The dictionary does not have to override all level names.
                To use the default names, use `level_names = {}`.
            parse_mode: The markup language that Telegram needs to parse to display formatted text.
                Defaults to `''` (Plain Text).
            escape_func: The function that will be used to escape special characters. By default,
                the function does not perform escaping.
            escape_message: If `True`(the default), escape the log message text.
            escape_stack_info: If `True` (the default), escape stack output.
            escape_exception: If `True` (the default), escape traceback exception output.
            escape_result: If `True`, escape the resulting message after all formatting. To enable
                this option, it is recommended to disable `escape_message`, `escape_stack_info`and
                `escape_exception` to avoid repeated escaping.
            stack_info_template: A template string with a single required parameter `{text}` for
                marking up stack info text. For example, `'<code>{text}</code>'` for HTML.
                By default, does not change the text.
            exception_template: A template string with a single required parameter `{text}` for
                marking up the traceback output. For example, `'<code>{text}</code>'` for HTML.
                By default, does not change the text.
            result_template: A template string with a single required parameter `{text}` for
                marking up the resulting message after all formatting. The `text` parameter
                includes the result of substitution into the `fmt` string, stack info and exception
                traceback. For example, `'<code>{text}</code>'` for HTML. By default, does not
                change the text.

        There is no separate `message_template` parameter in templates, since this functionality is
        implemented through the standard `fmt` string. For example, `fmt = '<code>{message}</code>'`.
        """

        super().__init__(
            fmt = fmt,
            datefmt = datefmt,
            style = style,
            validate = validate,
            defaults = defaults,
            level_names = level_names,
            parse_mode = parse_mode,
        )

        self._escape_func = escape_func
        self._escape_message = escape_message
        self._escape_stack_info = escape_stack_info
        self._escape_excpetion = escape_exception
        self._escape_result = escape_result
        self._stack_info_template = stack_info_template
        self._exception_template = exception_template
        self._result_template = result_template
    
    @override
    def formatMessage(self, record: LogRecord) -> str:
        if record.getMessage() and self._escape_message:
            record.msg = self._escape_func(record.getMessage())

        return super().formatMessage(record)

    @override
    def formatException(self, ei: SysExcInfoType) -> str:
        text = super().formatException(ei)

        if self._escape_excpetion:
            text = self._escape_func(text)

        text = self._exception_template.format(text=text)

        return text
    
    @override
    def formatStack(self, stack_info: str) -> str:
        text = super().formatStack(stack_info)

        if self._escape_stack_info:
            text = self._escape_func(text)

        text = self._stack_info_template.format(text=text)

        return text
    
    @override
    def _pre_format(self, record: LogRecord) -> None:
        if record.getMessage() and self._escape_message:
            record.msg = self._escape_func(record.getMessage())

        super()._pre_format(record)

    @override
    def _post_format(self, text: str) -> str:
        text = super()._post_format(text)

        if self._escape_result:
            text = self._escape_func(text)

        text = self._result_template.format(text=text)

        return text
