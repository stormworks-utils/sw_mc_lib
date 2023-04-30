from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generator

from .util import generic_str
from .XMLParser import XMLParserElement


class XMLElement(ABC):
    @abstractmethod
    def to_xml(self) -> XMLParserElement:
        ...

    @staticmethod
    @abstractmethod
    def from_xml(element: XMLParserElement) -> XMLElement:
        ...

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
        return (i for i in dir(self) if not i.startswith("__"))
