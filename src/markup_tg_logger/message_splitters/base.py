from typing import override, List

from ..interfaces import IMessageSplitter
from ..config import MAX_MESSAGE_LENGTH


class BaseMessageSplitter(IMessageSplitter):
    def __init__(self) -> None:
        self._MAX_MESSAGE_LENGTH = MAX_MESSAGE_LENGTH
        self._PARSE_MODE = ''

    @property
    @override
    def parse_mode(self) -> str:
        return self._PARSE_MODE 

    @override
    def split(self, text: str) -> List[str]:
        return [text[index:index+self._MAX_MESSAGE_LENGTH] for index in range(0, len(text), self._MAX_MESSAGE_LENGTH)] 
    
