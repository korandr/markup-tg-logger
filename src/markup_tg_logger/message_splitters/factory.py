from ..exceptions import NotMappedSplitterError
from ..interfaces import IMessageSplitter
from ..resolve_object_from_config import resolve_object_from_config
from ..types import ParseMode
from .base import BaseMessageSplitter
from .html import HtmlMessageSplitter


ParseModeToSplitter = dict[ParseMode, IMessageSplitter | dict]

class MessageSplitterFactory:
    """Splitter factory.
    
    Provides a splitter implementation depending on the markup language.
    """

    def __init__(
        self,
        parse_mode_to_splitter: ParseModeToSplitter | None = None,
    ) -> None:
        """
        Args:
            parse_mode_to_splitter: Splitter mapping for each supported markup language. If `None`,
                then splitters will be assigned for plain text (`''`) and HTML, as for the most
                popular options. To support configuration from a file, a dictionary can be
                specified instead of an `IMessageSplitter` instance. The dictionary must contain
                the `'()'` key with the import path for the requested class as a string. The
                remaining dictionary keys will be passed to the constructor of the specified class.
                For example: `{'()': 'markup_tg_logger.BaseMessageSplitter'}`.
        """

        self._parse_mode_to_splitter: dict[ParseMode, IMessageSplitter] = {}

        if parse_mode_to_splitter is None:
            self._parse_mode_to_splitter = {
                '': BaseMessageSplitter(),
                'HTML': HtmlMessageSplitter(), 
            }
        else:
            for parse_mode, splitter in parse_mode_to_splitter.items():
                if isinstance(splitter, dict):
                    resolved_spliter = resolve_object_from_config(
                        splitter,
                        IMessageSplitter, # type: ignore[type-abstract] 
                                          # https://github.com/python/mypy/issues/4717
                    )
                    self._parse_mode_to_splitter[parse_mode] = resolved_spliter
                else:
                    self._parse_mode_to_splitter[parse_mode] = splitter

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
    
