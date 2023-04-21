from __future__ import annotations

from sw_mc_lib.Component import Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.XMLElement import XMLElement
from sw_mc_lib.util import string_to_sw_float


class DropDownOption(XMLElement):
    def __init__(self, label: str, value_text: str):
        self.label: str = label
        self.value_text: str = value_text

    @staticmethod
    def from_xml(element: XMLParserElement) -> DropDownOption:
        assert element.tag == 'i', f'invalid DropDownOption {element}'
        label: str = element.attributes.get('l', '')
        value_text: str = '0'
        for child in element.children:
            assert child.tag == 'v', f'invalid value field for DropDownOption {element}'
            value_text = child.attributes.get('text', '0')
        return DropDownOption(label, value_text)

    def to_xml(self) -> str:
        xml: str = f'<i l={self.escape_string(self.label)}>\n'
        xml += self.indent(self._to_xml_number_field('v', self.value_text))
        xml += '</i>\n'
        return xml

    @property
    def value(self) -> float:
        return string_to_sw_float(self.value_text)

    @value.setter
    def value(self, value: float):
        self.value_text = str(value)


class PropertyDropdown(Component):
    def __init__(self, component_id: int, position: Position, selected: int, options: list[DropDownOption]):
        super().__init__(ComponentType.PropertyDropdown, component_id, position, 0.5)
        self.selected: int = selected
        self.options: list[DropDownOption] = options

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertyDropdown:
        assert element.tag == 'c', f'invalid PropertyDropdown {element}'
        assert element.attributes.get('type', '0') == str(
            ComponentType.PropertyDropdown.value
            ), f'Not an PropertyDropdown {element}'
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = PropertyDropdown._basic_in_parsing(obj)
        selected: int = int(obj.attributes.get('i', '0'))
        options: list[DropDownOption] = []
        for child in obj.children:
            if child.tag == 'items':
                for entry in child.children:
                    options.append(DropDownOption.from_xml(entry))
        return PropertyDropdown(component_id, position, selected, options)

    def _inner_to_xml(self) -> str:
        xml: str = f'i="{self.selected}"\n'
        xml += self.indent(self._pos_in_to_xml({}))
        items: str = '<items>\n'
        for option in self.options:
            items += self.indent(option.to_xml())
        items += '</items>\n'
        xml += self.indent(items)
        return xml
