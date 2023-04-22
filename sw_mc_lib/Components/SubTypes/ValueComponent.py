from __future__ import annotations

from abc import ABC

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.util import string_to_sw_float


class ValueComponent(Component, ABC):
    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
        value_text: str,
        **kwargs: str,
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.value_text: str = value_text

    @staticmethod
    def _basic_value_parsing(element: XMLParserElement) -> str:
        value_text: str = ValueComponent._basic_number_field_parsing(element, "r")
        return value_text

    def _value_to_xml(self) -> list[XMLParserElement]:
        return [self._to_xml_number_field("r", self.value_text)]

    @property
    def value(self) -> float:
        return string_to_sw_float(self.value_text)

    @value.setter
    def value(self, value: float) -> None:
        self.value_text = str(value)
