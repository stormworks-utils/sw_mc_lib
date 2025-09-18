from __future__ import annotations

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.NumberProperty import NumberInput, NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class PropertyNumber(Component):
    """
    Adds a custom number input that will be seen on the microcontroller's property panel when placed on a vehicle.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        name: str = "number",
        value_property: NumberInput = None,
    ):
        super().__init__(ComponentType.PropertyNumber, component_id, position)
        self.name: str = name
        self.value_property: NumberProperty = NumberProperty.from_input(
            value_property, "v"
        )

    @property
    def height(self) -> float:
        return 0.5

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyNumber:
        obj: XMLParserElement = element.children[0]
        component_id, position, _, properties = Component._basic_in_parsing(obj)
        name: str = obj.attributes.get("n", "number")
        return PropertyNumber(component_id, position, name, properties.get("v"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml(
            properties={"v": self.value_property}
        )
        return {"n": self.name}, children
