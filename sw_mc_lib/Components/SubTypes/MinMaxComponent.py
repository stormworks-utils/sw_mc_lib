from __future__ import annotations

from abc import ABC

from sw_mc_lib.Component import Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.util import string_to_sw_float


class MinMaxComponent(Component, ABC):
    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
        min_text: str,
        max_text: str,
        **kwargs
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.min_text: str = min_text
        self.max_text: str = max_text

    @staticmethod
    def _basic_min_max_parsing(element: XMLParserElement) -> tuple[str, str]:
        min_text: str = MinMaxComponent._basic_number_field_parsing(element, 'min')
        max_text: str = MinMaxComponent._basic_number_field_parsing(element, 'max')
        return min_text, max_text

    def _min_max_to_xml(self) -> str:
        xml = self._to_xml_number_field('min', self.min_text)
        xml += self._to_xml_number_field('max', self.max_text)
        return xml

    @property
    def min(self) -> float:
        return string_to_sw_float(self.min_text)

    @min.setter
    def min(self, value: float):
        self.min_text = str(value)

    @property
    def max(self) -> float:
        return string_to_sw_float(self.max_text)

    @max.setter
    def max(self, value: float):
        self.max_text = str(value)
