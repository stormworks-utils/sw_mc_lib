from __future__ import annotations

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class PropertyToggle(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        name: str,
        on_label: str,
        off_label: str,
        value: bool,
    ):
        super().__init__(ComponentType.PropertyToggle, component_id, position, 0.5)
        self.name: str = name
        self.on_label: str = on_label
        self.off_label: str = off_label
        self.value: bool = value

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyToggle:
        assert element.tag == "c", f"invalid PropertyToggle {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PropertyToggle.value
        ), f"Not an PropertyToggle {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = PropertyToggle._basic_in_parsing(obj)
        name: str = obj.attributes.get("n", "toggle")
        on_label: str = obj.attributes.get("on", "on")
        off_label: str = obj.attributes.get("off", "off")
        value: bool = obj.attributes.get("v", "false") == "true"
        return PropertyToggle(component_id, position, name, on_label, off_label, value)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {
            "n": self.name,
            "on": self.on_label,
            "off": self.off_label,
            "v": str(self.value).lower(),
        }
        children: list[XMLParserElement] = self._pos_in_to_xml({})
        return attributes, children
