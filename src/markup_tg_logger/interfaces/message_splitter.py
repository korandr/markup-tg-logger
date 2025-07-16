from abc import ABC, abstractmethod

from ..types import ParseMode


class IMessageSplitter(ABC):
    """Text to message splitter interface."""

    @property
    @abstractmethod
    def parse_mode(self) -> ParseMode:
        """Supported markup language."""
    
    @abstractmethod
    def split(self, text: str) -> list[str]:
        """Split text into list of messages.
        
        Args:
            text: Source text to split.

        Raises:
            SplitterException: Base exception when working with a splitter.
        """
