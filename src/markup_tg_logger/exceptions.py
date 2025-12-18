class MarkupTgLoggerException(Exception):
    """Base library exception."""

class SenderError(MarkupTgLoggerException):
    """Base exception when working with the `ITelegramSender` implementation."""

class TelegramApiError(SenderError):
    """Subclass of `SenderError` for errors sent by Telegram server."""

class SplitterException(MarkupTgLoggerException):
    """Base exception when working with the `IMessageSplitter` implementation."""

class NotMappedSplitterError(SplitterException):
    """No splitter specified for selected markup language."""

class TagMismatchError(SplitterException):
    """The found closing tag does not match any opening tag in the stack."""

class ImpossibleToSplitError(SplitterException):
    """Unable to split text - markup length alone exceeds limit."""

    def __init__(self, parse_mode) -> None:
        super().__init__(f'{parse_mode} markup take up the entire length of the message')

class InvalidMarkupError(SplitterException):
    """The splitting text is invalid or not escaped."""

    def __init__(self, *, parse_mode: str, char: str, index: int, text: str) -> None:
        fragment_start_index = max(0, index - 5)
        fragment_end_index = min(len(text), index + 5)
        fragment = text[fragment_start_index:fragment_end_index]

        super().__init__(
            f'Invalid {parse_mode}. It looks like the text was escaped incorrectly.\n'
            f'Character: "{char}".\n'
            f'Character position index: {index}.\n'
            f'Text fragment with error: "{fragment}".\n'
            f'Full text:\n{text}'
        )
