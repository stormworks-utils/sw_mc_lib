from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generator

from .util import generic_str
from .XMLParser import XMLParserElement


class XMLElement(ABC):
    """
    An element that can be deserialized from and serialized to an XML element
    """

    @abstractmethod
    def to_xml(self) -> XMLParserElement:
        """
        Serialize the element to an XML element.

        :return: The XML element
        """

    @staticmethod
    @abstractmethod
    def from_xml(element: XMLParserElement) -> XMLElement:
        """
        Deserialize the element from an XML element.

        :param element: XML element
        :return: Deserialized element
        """

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
