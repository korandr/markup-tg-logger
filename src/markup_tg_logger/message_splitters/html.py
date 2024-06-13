from typing import override, List, Tuple, TypeAlias

from .base import BaseMessageSplitter


_HtmlUnits: TypeAlias = List[str]

class ImpossibleSplitError(Exception):
    def __init__(self) -> None:
        super().__init__('HTML markup take up the entire length of the message')

class HtmlTag:
    def __init__(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        self._tag = tag
        self._attrs = attrs

    @property
    def tag_only(self) -> str:
        return self._tag

    @property
    def start_tag(self) -> str:
        attrs_text = ' '.join([f'{attr[0]}="{attr[1]}"' for attr in self._attrs])

        return f'<{self._tag}>' if attrs_text == '' else f'<{self._tag} {attrs_text}>'
    
    @property
    def end_tag(self) -> str:
        return f'</{self._tag}>'



class HtmlMessageSplitter(BaseMessageSplitter):
    def __init__(self):
        super().__init__()
        self._PARSE_MODE = 'HTML'

        self._parts: List[str] = []
        self._current_part: _HtmlUnits = []
        self._stack: List[HtmlTag] = []

    @override
    def split(self, text:str):
        self._start_parsing(text)
        parts = self._parts
        self._reset()

        return parts
    
    def _start_parsing(self, data: str) -> None:
        while '>' in data:
            index = data.index('<')
            pop, data = data[:index], data[index+1:]
            if pop != '': self._handle_data(pop)
            index = data.index('>')
            pop, data = data[:index], data[index+1:]
            if pop[0] == '/':
                self._handle_endtag(pop[1:])
            else:
                elements = pop.split(' ')
                attrs = []
                tag = elements[0]
                if len(elements) > 1:
                    for element in elements[1:]:
                        attr_0, attr_1 = element.split('=')
                        attr_1 = attr_1[1:-1]
                        attrs.append((attr_0, attr_1))

                self._handle_starttag(tag, attrs)

        if data != '':
            self._handle_data(data)
        self._split()

    def _handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        html_tag = HtmlTag(tag, attrs)
        self._stack.append(html_tag)
        self._current_part.append(html_tag.start_tag)

        if self._length_over_limit >= 0:
            current_tag = self._stack.pop()
            current_unit = self._current_part.pop()

            self._split()

            self._stack.append(current_tag)
            self._current_part.append(current_unit)

            if self._length_over_limit >= 0: raise ImpossibleSplitError
 
    def _handle_endtag(self, tag:str) -> None:
        if len(self._stack) == 0 or self._stack[-1].tag_only != tag: raise ValueError('Invalid HTML: tag mismatch')

        tag: HtmlTag = self._stack.pop()
        self._current_part.append(tag.end_tag)

    def _handle_data(self, data: str) -> None:
        self._current_part.append(data)

        length_over_limit = self._length_over_limit
        while length_over_limit > 0:
            data = self._current_part.pop()

            delta = length_over_limit

            current_data = data[:-delta]
            next_data = data[-delta:]

            self._current_part.append(current_data)
            self._split()

            self._current_part.append(next_data)
            length_over_limit = self._length_over_limit


    def _reset(self) -> None:
        self._parts = []
        self._current_part = []
        self._stack = []

    @property
    def _close_units(self) -> _HtmlUnits:
        close_units: _HtmlUnits = []        
        for tag in self._stack:
            close_units.append(tag.end_tag)

        close_units.reverse()

        return close_units

    @property
    def _closed_current_part(self) -> _HtmlUnits:
        return self._current_part + self._close_units

    def _units_to_str(self, units: _HtmlUnits) -> int:
        return ''.join(units)
    
    @property
    def _length_over_limit(self) -> int:
        closed_part = self._closed_current_part

        return len(self._units_to_str(closed_part)) - self._MAX_MESSAGE_LENGTH

    def _split(self) -> None:
        closed_part = self._closed_current_part
        closed_part_str = self._units_to_str(closed_part)

        if closed_part_str == '': raise ImpossibleSplitError

        self._parts.append(closed_part_str)

        self._current_part = []
        
        for tag in self._stack:
            self._current_part.append(tag.start_tag)

