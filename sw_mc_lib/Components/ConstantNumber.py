from __future__ import annotations

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.util import string_to_sw_float


class Abs(Component):
    def __init__(self, component_id: int, position: Position, value_text: str):
        super().__init__(ComponentType.Abs, component_id, position, 0.5)
        self.value_text: str = value_text

    @staticmethod
    def from_xml(element: XMLParserElement) -> Abs:
        assert element.tag == "c", f"invalid Abs {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Abs.value
        ), f"Not an Abs {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = Abs._basic_in_parsing(obj)
        value_text: str = Abs._basic_number_field_parsing(obj, "n")
        return Abs(component_id, position, value_text)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml()
        children.append(self._to_xml_number_field("n", self.value_text))
        return {}, children

    @property
    def value(self) -> float:
        return string_to_sw_float(self.value_text)

    @value.setter
    def value(self, value: float) -> None:
        self.value_text = str(value)
