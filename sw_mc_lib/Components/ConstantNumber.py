from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement

from .SubTypes.ValueComponent import ValueComponent


class ConstantNumber(ValueComponent):
    """
    Outputs a constant number that is set on the properties panel.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        value_property: Optional[NumberProperty] = None,
    ):
        super().__init__(
            ComponentType.ConstantNumber, component_id, position, 0.5, value_property
        )

    @staticmethod
    def from_xml(element: XMLParserElement) -> ConstantNumber:
        assert element.tag == "c", f"invalid ConstantNumber {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.ConstantNumber.value
        ), f"Not an ConstantNumber {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, _, properties = ConstantNumber._basic_in_parsing(obj)
        value_property = ValueComponent._basic_value_parsing(properties)
        return ConstantNumber(component_id, position, value_property)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml()
        children.extend(self._value_to_xml())
        return {}, children
