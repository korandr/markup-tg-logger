from abc import ABC, abstractmethod
from typing import List


class IMessageSplitter(ABC):
    @property
    @abstractmethod
    def parse_mode(self) -> str: pass
    
    @abstractmethod
    def split(self, text: str) -> List[str]: pass

