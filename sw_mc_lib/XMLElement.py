from __future__ import annotations

from abc import ABC, abstractmethod
from inspect import Signature, signature
from typing import Any

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
        self_signature: Signature = signature(self.__init__)  # type: ignore
        return all(
            hasattr(other, name) and getattr(self, name) == getattr(other, name)
            for name in self_signature.parameters.keys()
        )
