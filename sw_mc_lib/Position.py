from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .XMLParser import XMLParserElement

from .XMLElement import XMLElement


class Position(XMLElement):
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    @staticmethod
    def from_xml(element: XMLParserElement) -> Position:
        assert element.tag == 'pos', f'Invalid node position {element}'
        return Position(
            float(element.attributes.get('x', '0')),
            float(element.attributes.get('y', '0')),
        )

    @staticmethod
    def empty_pos() -> Position:
        return Position(0.0, 0.0)

    def to_xml(self) -> str:
        xml: str = '<pos '
        if self.x != 0:
            xml += f'x="{self.x}" '
        if self.y != 0:
            xml += f'y="{self.y}" '
        return xml[:-1] + '/>\n'