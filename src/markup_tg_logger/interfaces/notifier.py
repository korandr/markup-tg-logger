from abc import ABC, abstractmethod
from logging import LogRecord


class INotifier(ABC):
    """Notification managment abstraction. 

    Class provides `disable_notification` parameter for Telegram `sendMessage` method depending
    on logger `LogRecord`.
    """

    @abstractmethod
    def disable_notification(self, record: LogRecord) -> bool:
        """Determine whether to disable notifications for this log record."""
