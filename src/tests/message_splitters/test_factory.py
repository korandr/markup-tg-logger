"""Test the `MessageSplitterFactory`."""

import pytest
from typing import override

from markup_tg_logger.exceptions import NotMappedSplitterError
from markup_tg_logger.interfaces import IMessageSplitter
from markup_tg_logger.message_splitters.factory import MessageSplitterFactory
from markup_tg_logger.types import ParseMode


class FakeSplitter(IMessageSplitter):
    @property
    @override
    def parse_mode(self) -> ParseMode:
        return ''
    
    @override
    def split(self, text: str) -> list[str]:
        return []

class SplitterA(FakeSplitter): pass
class SplitterB(FakeSplitter): pass


@pytest.mark.unit()
def test_factory_get() -> None:
    factory = MessageSplitterFactory(
        parse_mode_to_splitter = {
            '': SplitterA(),
            'HTML': SplitterB(),
        }
    )

    splitter = factory.get(parse_mode='')
    assert isinstance(splitter, SplitterA)

    splitter = factory.get(parse_mode='HTML')
    assert isinstance(splitter, SplitterB)

    with pytest.raises(NotMappedSplitterError):
        factory.get(parse_mode='Markdown')
