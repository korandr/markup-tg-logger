from logging import LogRecord, _nameToLevel
from typing import override

from ..interfaces import INotifier
from ..types import LogLevel


class LevelNotifier(INotifier):
    """Notifier depending on logging level.
    
    Notifications are enabled if the logging level is greater
    than or equal to the level specified in the constructor.
    """

    def __init__(self, level: LogLevel) -> None:
        """
        Args:
            level: Notifications are enabled if the logging level is greater
                than or equal to the level specified in the constructor.
        """

        if isinstance(level, str):
            level = _nameToLevel[level]

        self._level = level

    @override
    def disable_notification(self, record: LogRecord) -> bool:
        return True if record.levelno < self._level else False
