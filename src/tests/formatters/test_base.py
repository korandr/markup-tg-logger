"""Test the `BaseMarkupFormatter`."""

import logging
import pytest

from markup_tg_logger.formatters.base import BaseMarkupFormatter


@pytest.mark.unit()
def test_parse_mode() -> None:
    PARSE_MODE = 'HTML'
    formatter = BaseMarkupFormatter(parse_mode='HTML')

    assert formatter.parse_mode == PARSE_MODE

@pytest.mark.unit()
def test_level_names() -> None:
    DEBUG = 'test_debug'
    INFO = 'test_info'
    WARNING_DEFAULT = logging._levelToName[logging.WARNING]
    LEVEL_NAMES = {logging.DEBUG: DEBUG, logging.INFO: INFO}

    debug_record = logging.makeLogRecord({
        'name': 'test_logger',
        'levelno': logging.DEBUG,
        'levelname': logging._levelToName[logging.DEBUG],
    })

    warning_record = logging.makeLogRecord({
        'name': 'test_logger',
        'levelno': logging.WARNING,
        'levelname': logging._levelToName[logging.WARNING],
    })

    formatter = BaseMarkupFormatter(fmt='{levelname}', style='{', level_names=LEVEL_NAMES)

    debug_text = formatter.format(debug_record)
    warning_text = formatter.format(warning_record)

    assert debug_text == DEBUG
    assert warning_text == WARNING_DEFAULT
