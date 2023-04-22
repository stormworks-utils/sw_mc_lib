from __future__ import annotations

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from .SubTypes.ValueComponent import ValueComponent


class PropertyNumber(ValueComponent):
    def __init__(
        self, component_id: int, position: Position, name: str, value_text: str
    ):
        super().__init__(
            ComponentType.PropertyNumber, component_id, position, 0.5, value_text
        )
        self.name: str = name

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyNumber:
        assert element.tag == "c", f"invalid PropertyNumber {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PropertyNumber.value
        ), f"Not an PropertyNumber {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = PropertyNumber._basic_in_parsing(obj)
        name: str = obj.attributes.get("n", "number")
        value_text: str = PropertyNumber._basic_value_parsing(obj)
        return PropertyNumber(component_id, position, name, value_text)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml({})
        children.extend(self._value_to_xml())
        return {}, children
