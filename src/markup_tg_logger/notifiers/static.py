from logging import LogRecord

from ..interfaces import INotifier


class StaticNotifier(INotifier):
    def __init__(self, disable_notification: bool = False) -> None:
        self._disable_notification = disable_notification

    def is_disable_notification(self, record: LogRecord) -> bool:
        return self._disable_notification
    
