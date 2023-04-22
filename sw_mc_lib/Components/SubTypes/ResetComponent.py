from __future__ import annotations

from abc import ABC

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.util import string_to_sw_float


class ResetComponent(Component, ABC):
    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
        reset_text: str,
        **kwargs,
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.reset_text: str = reset_text

    @staticmethod
    def _basic_reset_parsing(element: XMLParserElement) -> str:
        reset_text: str = ResetComponent._basic_number_field_parsing(element, "r")
        return reset_text

    def _reset_to_xml(self) -> list[XMLParserElement]:
        return [self._to_xml_number_field("r", self.reset_text)]

    @property
    def reset(self) -> float:
        return string_to_sw_float(self.reset_text)

    @reset.setter
    def reset(self, value: float):
        self.reset_text = str(value)
