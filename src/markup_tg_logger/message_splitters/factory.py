from ..interfaces import IMessageSplitter
from ..exceptions import NotMappedSplitterError
from ..types import ParseMode
from .base import BaseMessageSplitter
from .html import HtmlMessageSplitter


class MessageSplitterFactory:
    """Splitter factory.
    
    Provides a splitter implementation depending on the markup language.
    """

    def __init__(
        self,
        parse_mode_to_splitter: dict[ParseMode, IMessageSplitter] | None = None,
    ) -> None:
        """
        Args:
            parse_mode_to_splitter: Splitter mapping for each supported markup language. If `None`,
                then splitters will be assigned for plain text (`''`) and HTML, as for the most
                popular options. 
        """

        if parse_mode_to_splitter is None:
            parse_mode_to_splitter = {
                '': BaseMessageSplitter(),
                'HTML': HtmlMessageSplitter(), 
            }

        self._parse_mode_to_splitter = parse_mode_to_splitter

    def get(self, parse_mode: ParseMode) -> IMessageSplitter:
        """Get splitter instance depending on `parse_mode`.
        
        Args:
            parse_mode: The markup language for which the splitter is needed.
        
        Raises:
            NotMappedSplitterError: No splitter specified for selected markup language.
        """

        splitter = self._parse_mode_to_splitter.get(parse_mode)
        if splitter is None:
            raise NotMappedSplitterError(f'No splitter specified for {parse_mode = }.')
        
        return splitter
    
