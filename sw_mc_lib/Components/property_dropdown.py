from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.NumberProperty import NumberInput, NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLElement import XMLElement
from sw_mc_lib.XMLParser import XMLParserElement


class DropDownOption(XMLElement):
    """
    A single Option for :class:`sw_mc_lib.Components.PropertyDropDown.PropertyDropDown`
    """

    def __init__(self, label: str, value_property: NumberInput = None):
        self.label: str = label
        self.value_property: NumberProperty = NumberProperty.from_input(
            value_property, "v"
        )

    @staticmethod
    def from_xml(element: XMLParserElement) -> DropDownOption:
        label: str = element.attributes.get("l", "")
        value_property: Optional[NumberProperty] = None
        for child in element.children:
            assert child.tag == "v", f"invalid value field for DropDownOption {element}"
            value_property = NumberProperty.from_xml(child)
        return DropDownOption(label, value_property)

    def to_xml(self) -> XMLParserElement:
        return XMLParserElement("i", {"l": self.label}, [self.value_property.to_xml()])

    def __hash__(self) -> int:
        return hash((self.label, self.value_property))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DropDownOption):
            return NotImplemented
        return self.label == other.label and self.value_property == other.value_property


class PropertyDropdown(Component):
    """
    Adds a custom dropdown list that will be seen on the microcontroller's property panel when placed on a vehicle.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        selected_property: int = 0,
        options: Optional[list[DropDownOption]] = None,
        name: str = "value",
    ):
        super().__init__(ComponentType.PropertyDropdown, component_id, position)
        self.selected_property: int = selected_property
        self.options: list[DropDownOption] = options or []
        self.name: str = name

    @property
    def height(self) -> float:
        return 0.5

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyDropdown:
        obj: XMLParserElement = element.children[0]
        component_id, position, _, _ = Component._basic_in_parsing(obj)
        selected_property: int = int(obj.attributes.get("i", "0"))
        name: str = obj.attributes.get("name", "value")
        options: list[DropDownOption] = []
        for child in obj.children:
            if child.tag == "items":
                for entry in child.children:
                    options.append(DropDownOption.from_xml(entry))
        return PropertyDropdown(
            component_id, position, selected_property, options, name
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {
            "i": str(self.selected_property),
            "name": self.name,
        }
        children: list[XMLParserElement] = self._pos_in_to_xml()
        items: XMLParserElement = XMLParserElement("items")
        for option in self.options:
            items.children.append(option.to_xml())
        children.append(items)
        return attributes, children
