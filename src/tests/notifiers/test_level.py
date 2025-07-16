"""Test the `LevelNotifier`."""

import logging
import pytest

from markup_tg_logger.notifiers.level import LevelNotifier
from .test_static import make_log_record_with_level


@pytest.mark.unit()
def test_disable_notification() -> None:
    notifier = LevelNotifier(level=logging.WARNING)

    assert notifier.disable_notification(make_log_record_with_level(logging.DEBUG)) == True
    assert notifier.disable_notification(make_log_record_with_level(logging.INFO)) == True
    assert notifier.disable_notification(make_log_record_with_level(logging.WARNING)) == False
    assert notifier.disable_notification(make_log_record_with_level(logging.ERROR)) == False
    assert notifier.disable_notification(make_log_record_with_level(logging.CRITICAL)) == False
    
