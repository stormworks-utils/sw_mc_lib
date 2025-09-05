from __future__ import annotations

import ctypes
from typing import Optional

from .XMLElement import XMLElement, XMLParserElement


def string_to_sw_float(to_convert: str) -> float:
    """
    Converts a number string to a float like the game does right now.

    :param to_convert: The string containing a float number
    :return: The resulting float
    """
    return float(f"{ctypes.c_float(float(to_convert)).value:0.6f}")


class NumberProperty(XMLElement):
    """
    A property with a numerical value. Stores the number as string to preserve full precision and
    leading/trailing zeroes. Name is how it is referred to by the game, and will be filled in upon serializing.
    """

    def __init__(self, text: str, name: Optional[str] = None):
        self.text: str = text
        self.name: str = name or "temp"

    @staticmethod
    def from_xml(element: XMLParserElement) -> NumberProperty:
        name: str = element.tag
        text: str = element.attributes.get("text", "0")
        return NumberProperty(text, name)

    def to_xml(self) -> XMLParserElement:
        return XMLParserElement(
            self.name, {"text": self.text, "value": str(self.value)}
        )

    @property
    def value(self) -> float:
        """
        The value of the text field as float property.

        :return: Float of text
        """
        return string_to_sw_float(self.text)

    @value.setter
    def value(self, value: float) -> None:
        self.text = str(value)

    @staticmethod
    def from_input(value: NumberInput, name: str, default: str = "0") -> NumberProperty:
        """Get a NumberProperty from either a NumberProperty or a number. Generate a default if None."""
        if isinstance(value, NumberProperty):
            value.name = name
            return value
        if isinstance(value, (int, float, str)):
            return NumberProperty(str(value), name)
        return NumberProperty(default, name)

    def __hash__(self) -> int:
        return hash(self.text)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NumberProperty):
            return False
        return self.text == other.text


NumberInput = Optional[NumberProperty | int | float | str]
