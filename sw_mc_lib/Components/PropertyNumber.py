from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement

from .SubTypes.ValueComponent import ValueComponent


class PropertyNumber(ValueComponent):
    """
    Adds a custom number input that will be seen on the microcontroller's property panel when placed on a vehicle.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        name: str = "number",
        value_property: Optional[NumberProperty] = None,
    ):
        super().__init__(
            ComponentType.PropertyNumber, component_id, position, 0.5, value_property
        )
        self.name: str = name

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyNumber:
        assert element.tag == "c", f"invalid PropertyNumber {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PropertyNumber.value
        ), f"Not an PropertyNumber {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, _, properties = PropertyNumber._basic_in_parsing(obj)
        name: str = obj.attributes.get("n", "number")
        value_property = PropertyNumber._basic_value_parsing(properties)
        return PropertyNumber(component_id, position, name, value_property)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml()
        children.extend(self._value_to_xml())
        return {}, children
