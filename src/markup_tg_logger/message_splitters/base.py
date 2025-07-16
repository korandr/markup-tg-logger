from typing import override

from ..config import MAX_MESSAGE_LENGTH
from ..interfaces import IMessageSplitter
from ..types import ParseMode


class BaseMessageSplitter(IMessageSplitter):
    """A simple text splitter for messages that do not exceed a given length limit.

    Splits messages into parts exactly according to the limit without taking into account the
    markup features. To customize the splitting process, you need to create a derived class
    and override the `split` method.
    """

    def __init__(
        self,
        max_message_length: int = MAX_MESSAGE_LENGTH,
        parse_mode: ParseMode = ''
    ) -> None:
        """
        Args: 
            max_message_length: The maximum number of characters allowed in one message.
            parse_mode: Text markup language. In this implementation, it does not affect
                the splitting process.
        """

        self._max_message_length = max_message_length
        self._parse_mode: ParseMode = parse_mode

    @property
    @override
    def parse_mode(self) -> ParseMode:
        return self._parse_mode

    @override
    def split(self, text: str) -> list[str]:
        return [text[i : i + self._max_message_length] for i in range(0, len(text), self._max_message_length)] 
    
