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
