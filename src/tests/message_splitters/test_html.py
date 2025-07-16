"""Test the `HtmlMessageSplitter`."""

import pytest

from markup_tg_logger.exceptions import SplitterException
from markup_tg_logger.message_splitters.html import HtmlMessageSplitter


@pytest.mark.unit()
def test_no_markup() -> None:
    limit = 10

    text_1 = 'a' * limit
    text_2 = 'b' * limit
    text_3 = 'c' * (limit // 2)

    splitter = HtmlMessageSplitter(max_message_length=limit)
    messages = splitter.split(text_1 + text_2 + text_3)

    assert messages == [text_1, text_2, text_3]

@pytest.mark.unit()
def test_simple_html() -> None:
    limit = 10
    text = '12345<b>12345</b>12345'
    
    splitter = HtmlMessageSplitter(max_message_length=limit)
    messages = splitter.split(text)

    assert messages == ['12345', '<b>123</b>', '<b>45</b>1', '2345']

@pytest.mark.unit()
def test_crossing_tags() -> None:
    limit = 20
    text = '12345<a>1234567890<b>1234567890</a>1234567890</b>12345'

    splitter = HtmlMessageSplitter(max_message_length=limit)
    messages = splitter.split(text)

    assert messages == [
        '12345<a>12345678</a>',
        '<a>90<b>1234</b></a>',
        '<a><b>567890</a></b>',
        '<b>1234567890</b>123',
        '45',
    ]

@pytest.mark.unit()
def test_end_tag_without_start_tag() -> None:
    limit = 10
    text = 'sample text </endtag> sample text'
    
    splitter = HtmlMessageSplitter(max_message_length=limit)

    with pytest.raises(SplitterException):
        splitter.split(text)

@pytest.mark.unit()
def test_start_tag_without_end_tag() -> None:
    limit = 10
    text = '12345<b>12345'
    
    splitter = HtmlMessageSplitter(max_message_length=limit)
    messages = splitter.split(text)

    assert messages == ['12345', '<b>123</b>', '<b>45</b>']

@pytest.mark.unit()
def test_markup_only() -> None:
    text = '<a><b><c></c></b></a>'
    limit = len(text) + 1
    
    splitter = HtmlMessageSplitter(max_message_length=limit)
    messages = splitter.split(text)

    assert messages == [text]

@pytest.mark.unit()
def test_limit_too_small() -> None:
    text = '<a><b><c></c></b></a>'
    limit = len(text)
    
    splitter = HtmlMessageSplitter(max_message_length=limit)
    
    with pytest.raises(SplitterException):
        splitter.split(text)
