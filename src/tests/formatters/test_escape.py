"""Test the `EscapeMarkupFormatter`."""

import html
import logging
import pytest

from markup_tg_logger.formatters.escape import EscapeMarkupFormatter


HTML_TEXT = '<code>test text</code>'
PLAIN_TEXT = 'test text'
ESCAPED_TEXT = '&lt;code&gt;test text&lt;/code&gt;'

HTML_TEMPLATE = '<tag>{text}</tag>'

@pytest.mark.unit()
def make_log_record(msg: str = '', stack_info: str = '', exc_info: str = '') -> logging.LogRecord:
    """Make a `LogRecord` for tests."""

    return logging.makeLogRecord({
        'name': 'test_logger',
        'levelno': logging.INFO,
        'levelname': logging._levelToName[logging.INFO],
        'msg': msg,
        'stack_info': stack_info,
        'exc_info': (ValueError, ValueError(exc_info), None) if exc_info else '',
    })

@pytest.mark.unit()
def test_escape_message_stack_and_exception() -> None:
    formatter = EscapeMarkupFormatter(
        fmt = '{message}',
        style = '{',
        escape_func = lambda text: html.escape(text, quote=False),
        escape_message = True,
        escape_stack_info = True,
        escape_exception = True,
        escape_result = False,
    )

    message_record = make_log_record(msg=HTML_TEXT)
    stack_record = make_log_record(stack_info=HTML_TEXT)
    exc_record = make_log_record(exc_info=HTML_TEXT)

    message_text = formatter.format(message_record)
    stack_text = formatter.format(stack_record)
    exc_text = formatter.format(exc_record)

    assert message_text == ESCAPED_TEXT
    assert stack_text == '\n' + ESCAPED_TEXT
    assert exc_text == '\nValueError: ' + ESCAPED_TEXT

@pytest.mark.unit()
def test_no_escape_message_stack_and_exception() -> None:
    formatter = EscapeMarkupFormatter(
        fmt = '{message}',
        style = '{',
        escape_func = lambda text: html.escape(text, quote=False),
        escape_message = False,
        escape_stack_info = False,
        escape_exception = False,
        escape_result = False,
    )

    message_record = make_log_record(msg=HTML_TEXT)
    stack_record = make_log_record(stack_info=HTML_TEXT)
    exc_record = make_log_record(exc_info=HTML_TEXT)

    message_text = formatter.format(message_record)
    stack_text = formatter.format(stack_record)
    exc_text = formatter.format(exc_record)

    assert message_text == HTML_TEXT
    assert stack_text == '\n' + HTML_TEXT
    assert exc_text == '\nValueError: ' + HTML_TEXT

@pytest.mark.unit()
def test_escape_result() -> None:
    formatter = EscapeMarkupFormatter(
        fmt = '{message}',
        style = '{',
        escape_func = lambda text: html.escape(text, quote=False),
        escape_message = False,
        escape_stack_info = False,
        escape_exception = False,
        escape_result = True,
    )

    record = make_log_record(msg=HTML_TEXT, stack_info=HTML_TEXT, exc_info=HTML_TEXT)
    text = formatter.format(record)

    #              | -- message -- | ------- exception ------- | --- stack --- |
    assert text == f'{ESCAPED_TEXT}\nValueError: {ESCAPED_TEXT}\n{ESCAPED_TEXT}'

@pytest.mark.unit()
def test_stack_and_exception_templates() -> None:
    formatter = EscapeMarkupFormatter(
        fmt = '{message}',
        style = '{',
        escape_message = False,
        escape_stack_info = False,
        escape_exception = False,
        escape_result = False,
        exception_template = HTML_TEMPLATE,
        stack_info_template = HTML_TEMPLATE,
    )

    record = make_log_record(msg=PLAIN_TEXT, stack_info=PLAIN_TEXT, exc_info=PLAIN_TEXT)
    text = formatter.format(record)

    exception_text = HTML_TEMPLATE.format(text=f'ValueError: {PLAIN_TEXT}')
    stack_text = HTML_TEMPLATE.format(text=PLAIN_TEXT)

    assert text == f'{PLAIN_TEXT}\n{exception_text}\n{stack_text}'

@pytest.mark.unit()
def test_result_template() -> None:
    formatter = EscapeMarkupFormatter(
        fmt = '{message}',
        style = '{',
        escape_message = False,
        escape_stack_info = False,
        escape_exception = False,
        escape_result = False,
        result_template = HTML_TEMPLATE,
    )

    record = make_log_record(msg=PLAIN_TEXT, stack_info=PLAIN_TEXT, exc_info=PLAIN_TEXT)
    text = formatter.format(record)

    expected_text = f'{PLAIN_TEXT}\nValueError: {PLAIN_TEXT}\n{PLAIN_TEXT}'

    assert text == HTML_TEMPLATE.format(text=expected_text)
