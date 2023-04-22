from __future__ import annotations
from abc import ABC, abstractmethod

from .XMLParser import XMLParserElement
from .util import generic_str, string_to_sw_float


class XMLElement(ABC):
    @abstractmethod
    def to_xml(self) -> XMLParserElement:
        ...

    @staticmethod
    @abstractmethod
    def from_xml(element: XMLParserElement) -> XMLElement:
        ...

    @staticmethod
    def _to_xml_number_field(name: str, value: str) -> XMLParserElement:
        return XMLParserElement(
            name, {"text": value, "value": str(string_to_sw_float(value))}
        )

    def __repr__(self):
        return generic_str(self)
