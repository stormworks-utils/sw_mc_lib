from __future__ import annotations
from abc import ABC, abstractmethod

from .XMLParser import XMLParserElement
from .util import generic_str, string_to_sw_float


class XMLElement(ABC):
    INDENTATION_CHARACTER: str = "\t"

    @abstractmethod
    def to_xml(self) -> str:
        ...

    @staticmethod
    @abstractmethod
    def from_xml(element: XMLParserElement) -> XMLElement:
        ...

    @staticmethod
    def escape_string(to_escape: str) -> str:
        """
        Escapes a string so that it results in valid xml. To be used like following:

        `abc<>"def\n"` -> `'abc&lt;&gt;"def\n"'`
        """
        to_escape = to_escape.replace('&', '&amp;')
        to_escape = to_escape.replace('<', '&lt;')
        to_escape = to_escape.replace('>', '&gt;')
        if to_escape.count('"') > to_escape.count("'"):
            to_escape = to_escape.replace("'", '&apos;')
            to_escape = f"'{to_escape}'"
        else:
            to_escape = to_escape.replace('"', '&quot;')
            to_escape = f'"{to_escape}"'
        return to_escape

    @staticmethod
    def indent(to_indent: str) -> str:
        """
        Indents the string by one tab and adds a newline at the end

        `<node/>` -> `\t<node/>\n`
        """
        return '\n'.join(XMLElement.INDENTATION_CHARACTER + line for line in to_indent.rstrip().split('\n')) + '\n'

    @staticmethod
    def _to_xml_number_field(name: str, value: str) -> str:
        return f'<{name} text={XMLElement.escape_string(value)} value="{string_to_sw_float(value)}"/>\n'

    def __repr__(self):
        return generic_str(self)
