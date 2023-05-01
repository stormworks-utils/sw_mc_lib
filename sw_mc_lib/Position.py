from __future__ import annotations

from .XMLElement import XMLElement
from .XMLParser import XMLParserElement


class Position(XMLElement):
    """
    Position of a Component. Used in 0.25 intervals.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x: float = x
        self.y: float = y

    @staticmethod
    def from_xml(element: XMLParserElement) -> Position:
        assert element.tag == "pos", f"Invalid node position {element}"
        return Position(
            float(element.attributes.get("x", "0")),
            float(element.attributes.get("y", "0")),
        )

    def to_xml(self) -> XMLParserElement:
        attributes: dict[str, str] = {}
        if self.x != 0:
            attributes["x"] = str(self.x)
        if self.y != 0:
            attributes["y"] = str(self.y)
        return XMLParserElement("pos", attributes)
