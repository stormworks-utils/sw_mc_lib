from __future__ import annotations

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.XMLElement import XMLElement
from sw_mc_lib.NumberProperty import NumberProperty


class DropDownOption(XMLElement):
    def __init__(self, label: str, value: NumberProperty):
        self.label: str = label
        self.value: NumberProperty = value

    @staticmethod
    def from_xml(element: XMLParserElement) -> DropDownOption:
        assert element.tag == "i", f"invalid DropDownOption {element}"
        label: str = element.attributes.get("l", "")
        value: NumberProperty = NumberProperty("0", "v")
        for child in element.children:
            assert child.tag == "v", f"invalid value field for DropDownOption {element}"
            value = NumberProperty.from_xml(child)
        return DropDownOption(label, value)

    def to_xml(self) -> XMLParserElement:
        return XMLParserElement("i", {"l": self.label}, [self.value.to_xml()])


class PropertyDropdown(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        selected: int,
        options: list[DropDownOption],
    ):
        super().__init__(ComponentType.PropertyDropdown, component_id, position, 0.5)
        self.selected: int = selected
        self.options: list[DropDownOption] = options

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyDropdown:
        assert element.tag == "c", f"invalid PropertyDropdown {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PropertyDropdown.value
        ), f"Not an PropertyDropdown {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = PropertyDropdown._basic_in_parsing(
            obj
        )
        selected: int = int(obj.attributes.get("i", "0"))
        options: list[DropDownOption] = []
        for child in obj.children:
            if child.tag == "items":
                for entry in child.children:
                    options.append(DropDownOption.from_xml(entry))
        return PropertyDropdown(component_id, position, selected, options)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {"i": str(self.selected)}
        children: list[XMLParserElement] = self._pos_in_to_xml()
        items: XMLParserElement = XMLParserElement("items")
        for option in self.options:
            items.children.append(option.to_xml())
        children.append(items)
        return attributes, children
