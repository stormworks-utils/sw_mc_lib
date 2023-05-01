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
        super().__init__(ComponentType.PropertyText, component_id, position, 0.5)
        self.name: str = name
        self.value_property: str = value_property

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyText:
        assert element.tag == "c", f"invalid PropertyText {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PropertyText.value
        ), f"Not an PropertyText {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, _, _ = PropertyText._basic_in_parsing(obj)
        name: str = obj.attributes.get("n", "toggle")
        value_property: str = obj.attributes.get("v", "")
        return PropertyText(component_id, position, name, value_property)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {
            "n": self.name,
            "v": self.value_property,
        }
        children: list[XMLParserElement] = self._pos_in_to_xml()
        return attributes, children
