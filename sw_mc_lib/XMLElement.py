from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generator, Any

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

    def __repr__(self) -> str:
        return generic_str(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return all(
            callable(getattr(self, i)) or getattr(self, i) == getattr(other, i)
            for i in self.__dir()
        )

    def __dir(self) -> Generator[str, None, None]:
        return (i for i in self.__dir__() if not i.startswith("__"))
