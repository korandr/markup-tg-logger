"""Test the `StaticNotifier`."""

import logging
import pytest

from markup_tg_logger.notifiers.static import StaticNotifier


@pytest.mark.unit()
def make_log_record_with_level(level: int) -> logging.LogRecord:
    return logging.makeLogRecord({
        'name': 'test_logger',
        'levelno': level,
        'levelname': logging._levelToName[level],
    })

@pytest.mark.unit()
def test_disable_notification() -> None:
    notifier = StaticNotifier(disable_notification=True)

    assert notifier.disable_notification(make_log_record_with_level(logging.DEBUG)) == True
    assert notifier.disable_notification(make_log_record_with_level(logging.CRITICAL)) == True
    
