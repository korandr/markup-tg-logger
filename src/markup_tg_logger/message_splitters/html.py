from dataclasses import dataclass, field
from typing import override, TypeAlias

from ..config import MAX_MESSAGE_LENGTH
from ..exceptions import ImpossibleToSplitError, TagMismatchError
from .base import BaseMessageSplitter


HtmlNode: TypeAlias = str
HtmlAttribute: TypeAlias = tuple[str, str | None]


class HtmlTagContainer:
    """Container for HTML tag.

    Contains attributes. Does not contain the content of the element.
    """

    def __init__(self, tag_name: str, attrs: list[HtmlAttribute]) -> None:
        """
        Args:
            tag_name: Tag name without `<`, `>` and `/` symbols.
            attrs: HTML element attributes. Each attribute must be represented as a key-value pair.
                The value can be `None`.
        """

        self._tag_name = tag_name
        self._attrs = attrs

    @property
    def tag_name(self) -> str:
        """Tag name without `<`, `>` and `/` symbols."""

        return self._tag_name

    @property
    def start_tag(self) -> str:
        """Opening tag with attributes."""

        attrs_text = ' '.join([f'{attr[0]}="{attr[1]}"' for attr in self._attrs])

        return f'<{self._tag_name}>' if attrs_text == '' else f'<{self._tag_name} {attrs_text}>'
    
    @property
    def end_tag(self) -> str:
        """Closing tag."""

        return f'</{self._tag_name}>'


@dataclass
class SplitContext:
    """Current splitter operation data.
    
    Attributes:
        messages: List of already split messages that do not exceed the limit.
        current_message_nodes: A list of individual nodes from which the next message will be
            composed. The nodes are at the maximum nesting level. The closing tags are stored
            in the `stack`. To get the current message with closing tags, use the
            `complete_current_message_nodes()` method.
        stack: A quasi-LIFO stack of current HTML tags. LIFO may be violated when elements overlap.
            For example, `<b> bold <i> italic-bold </b> italic </i>`. 
    """

    messages: list[str] = field(default_factory = lambda: [])
    current_message_nodes: list[HtmlNode] = field(default_factory = lambda: [])
    stack: list[HtmlTagContainer] = field(default_factory = lambda: [])
    
    def complete_current_message_nodes(self) -> list[HtmlNode]:
        """Append closing tags to the current message's node list and return that list."""

        return self.current_message_nodes + self._compile_end_tags()
    
    def cut_current_message(self) -> None:
        """Move accumulated nodes of current message to finished messages.
        
        Raises:
            ImpossibleToSplitError: `current_message_nodes` empty.
        """

        completed_message_nodes = self.complete_current_message_nodes()
        completed_message = ''.join(completed_message_nodes)

        if completed_message == '':
            raise ImpossibleToSplitError(parse_mode='HTML')

        self.messages.append(completed_message)
        self.current_message_nodes = []
        
        for tag_container in self.stack:
            self.current_message_nodes.append(tag_container.start_tag)

    def _compile_end_tags(self) -> list[HtmlNode]:
        """Compile a list of closing tags from the stack."""

        nodes: list[HtmlNode] = [tag.end_tag for tag in self.stack]
        nodes.reverse()

        return nodes
    

class HtmlMessageSplitter(BaseMessageSplitter):
    """A text splitter with HTML markup for a list of messages not exceeding a given length limit.
    
    Each message contains all necessary opening and closing tags at the cut points. The length of
    messages does not exceed the limit taking into account the markup (before parsing entities).
    """

    def __init__(self, max_message_length: int = MAX_MESSAGE_LENGTH) -> None:
        """
        Args:
            max_message_length: The maximum number of characters allowed in one message.
        """

        super().__init__(max_message_length=max_message_length, parse_mode='HTML')

    @override
    def split(self, text: str) -> list[str]:
        context = SplitContext()
        self._start_parsing(text, context)

        return context.messages
    
    def _start_parsing(self, text: str, context: SplitContext) -> None:
        """Start parsing text with HTML markup.

        Args:
            text: Source text for parsing.
            context: Splitter operation data.

        Raises:
            ImpossibleToSplitError: Unable to split text - markup length alone exceeds limit.
            TagMismatchError: The found closing tag does not match any opening tag in the stack.
        """

        while '>' in text:
            # Text before the found tag.
            index = text.index('<')
            pop, text = text[:index], text[index+1:]
            if pop != '':
                self._handle_text_node(pop, context)

            # Text inside the tag.
            index = text.index('>')
            pop, text = text[:index], text[index+1:]

            if pop[0] == '/':
                self._handle_end_tag(tag_name=pop[1:], context=context)
            else:
                units = pop.split(' ')
                tag_name = units[0]
                attrs: list[HtmlAttribute] = []
                if len(units) > 1:
                    for unit in units[1:]:
                        attr_0, attr_1 = unit.split('=')
                        attr_1 = attr_1[1:-1]
                        attrs.append((attr_0, attr_1))

                self._handle_start_tag(tag_name, attrs, context)

        # Text after the last tag.
        if text != '':
            self._handle_text_node(text, context)

        # Create last message from rest.
        context.cut_current_message()

    def _handle_start_tag(self, tag_name: str, attrs: list[HtmlAttribute], context: SplitContext) -> None:
        """Process the found opening HTML tag.

        Create an instance of the `HtmlTagContainer` class and add it to the stack. If the current
        message exceeds the limit when opening and closing the added tag, then make a message cut.
        
        Args:
            tag_name: Tag name without `<`, `>` and `/` symbols.
            attrs: Tag attributes in key-value list format. Value can be `None`.
            context: Splitter operation data.

        Raises:
            ImpossibleToSplitError: Unable to split text - markup length alone exceeds limit.
        """

        tag_container = HtmlTagContainer(tag_name, attrs)
        context.stack.append(tag_container)
        context.current_message_nodes.append(tag_container.start_tag)

        # Check that the new opening tag does not immediately exceed the limit when closing.
        if self._get_length_over_limit(context) >= 0:
            current_tag = context.stack.pop()
            current_node = context.current_message_nodes.pop()

            context.cut_current_message()

            context.stack.append(current_tag)
            context.current_message_nodes.append(current_node)

            if self._get_length_over_limit(context) >= 0:
                raise ImpossibleToSplitError(parse_mode='HTML')
 
    def _handle_end_tag(self, tag_name: str, context: SplitContext) -> None:
        """Process the found closing HTML tag.

        Add a closing tag to the list of nodes in the current message and remove it from the stack.
        
        Args:
            tag_name: Tag name without `<`, `>` and `/` symbols.
            context: Splitter operation data.

        Raises:
            TagMismatchError: The found closing tag does not match any opening tag in the stack.
        """

        if len(context.stack) == 0:
            raise TagMismatchError(f'Invalid HTML. Extra closing tag found: {tag_name}')
        
        tag_names = [tag.tag_name for tag in context.stack]

        if tag_name not in tag_names:
            raise TagMismatchError(
                f'Invalid HTML. The closing tag </{tag_name}> does not have a corresponding '
                f'opening tag in the stack.'
            )
        
        # Find the index of the last occurrence of the corresponding opening tag in the stack.
        start_tag_index = len(tag_names) - 1 - tag_names[::-1].index(tag_name)

        # Extract a tag by index from the stack and add it to the current message.
        tag_container = context.stack.pop(start_tag_index)
        context.current_message_nodes.append(tag_container.end_tag)

    def _handle_text_node(self, text: str, context: SplitContext) -> None:
        """Process plain text inside or outside tags.
        
        Args:
            text: Text that does not contain markup.
            context: Splitter operation data.

        Raises:
            ImpossibleToSplitError: Unable to split text - markup length alone exceeds limit.
        """

        context.current_message_nodes.append(text)

        length_over_limit = self._get_length_over_limit(context)
        while length_over_limit > 0:
            text = context.current_message_nodes.pop()

            current_text = text[:-1*length_over_limit]
            next_text = text[-1*length_over_limit:]

            context.current_message_nodes.append(current_text)
            context.cut_current_message()

            context.current_message_nodes.append(next_text)
            length_over_limit = self._get_length_over_limit(context)

    def _get_length_over_limit(self, context: SplitContext) -> int:
        """Get the number of characters by which the current message exceeds the limit.
        
        Args:
            context: Splitter operation data.
        """

        closed_message_elements = context.complete_current_message_nodes()
        closed_message_str = ''.join(closed_message_elements)

        return len(closed_message_str) - self._max_message_length
