from __future__ import annotations

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class PropertyText(Component):
    """
    Adds a custom text input that will be seen on the microcontroller's property panel when placed on a vehicle,
    for showing player-defined text within a lua script.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        name: str = "Label",
        value_property: str = "",
    ):
        super().__init__(ComponentType.PropertyText, component_id, position)
        self.name: str = name
        self.value_property: str = value_property

    @property
    def height(self) -> float:
        return 0.5

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyText:
        obj: XMLParserElement = element.children[0]
        component_id, position, _, _ = Component._basic_in_parsing(obj)
        name: str = obj.attributes.get("n", "Label")
        value_property: str = obj.attributes.get("v", "")
        return PropertyText(component_id, position, name, value_property)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {
            "n": self.name,
            "v": self.value_property,
        }, self._pos_in_to_xml()
