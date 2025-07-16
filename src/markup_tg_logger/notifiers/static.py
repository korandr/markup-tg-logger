from logging import LogRecord
from typing import override

from ..interfaces import INotifier


class StaticNotifier(INotifier):
    """Notifier with constant value."""

    def __init__(self, disable_notification: bool = False) -> None:
        self._disable_notification = disable_notification

    @override
    def disable_notification(self, record: LogRecord) -> bool:
        return self._disable_notification
    
