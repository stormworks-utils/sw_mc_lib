from __future__ import annotations

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class PropertyToggle(Component):
    """
    Adds a custom on/off toggle that will be seen on the microcontroller's property panel when placed on a vehicle.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        name: str = "toggle",
        on_label: str = "on",
        off_label: str = "off",
        value_property: bool = False,
    ):
        super().__init__(ComponentType.PropertyToggle, component_id, position)
        self.name: str = name
        self.on_label: str = on_label
        self.off_label: str = off_label
        self.value_property: bool = value_property

    @property
    def height(self) -> float:
        return 0.75

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyToggle:
        obj: XMLParserElement = element.children[0]
        component_id, position, _, _ = Component._basic_in_parsing(obj)
        name: str = obj.attributes.get("n", "toggle")
        on_label: str = obj.attributes.get("on", "on")
        off_label: str = obj.attributes.get("off", "off")
        value_property: bool = obj.attributes.get("v", "false") == "true"
        return PropertyToggle(
            component_id, position, name, on_label, off_label, value_property
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {
            "n": self.name,
            "on": self.on_label,
            "off": self.off_label,
            "v": str(self.value_property).lower(),
        }, self._pos_in_to_xml()
