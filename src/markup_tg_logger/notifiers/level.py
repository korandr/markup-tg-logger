from logging import LogRecord

from ..interfaces import INotifier
from ..types import LoggerLevel

    
class LevelNotifier(INotifier):
    def __init__(self, level: LoggerLevel) -> None:
        self._level = level

    def is_disable_notification(self, record: LogRecord) -> bool:
        return True if record.levelno < self._level else False

