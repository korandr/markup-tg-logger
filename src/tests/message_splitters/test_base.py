"""Test the `BaseMessageSplitter`."""

import pytest

from markup_tg_logger.message_splitters.base import BaseMessageSplitter


@pytest.mark.unit()
def test_split_long_text() -> None:
    limit = 10

    text_1 = 'a' * limit
    text_2 = 'b' * limit
    text_3 = 'c' * (limit // 2)

    splitter = BaseMessageSplitter(max_message_length=limit)
    messages = splitter.split(text_1 + text_2 + text_3)

    assert messages == [text_1, text_2, text_3]

@pytest.mark.unit()
def test_split_less_then_limit() -> None:
    limit = 10
    text = 'a' * (limit // 2)

    splitter = BaseMessageSplitter(max_message_length=limit)
    messages = splitter.split(text)

    assert messages[0] == text
