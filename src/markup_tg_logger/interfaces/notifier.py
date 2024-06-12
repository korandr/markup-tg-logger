from abc import ABC, abstractmethod
from logging import LogRecord


class INotifier(ABC):
    @abstractmethod
    def is_disable_notification(self, record:LogRecord) -> bool: pass

