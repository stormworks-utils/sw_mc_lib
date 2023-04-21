from __future__ import annotations

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.util import string_to_sw_float
from .SubTypes.MinMaxComponent import MinMaxComponent
from .SubTypes.ValueComponent import ValueComponent


class PropertySlider(MinMaxComponent, ValueComponent):
    def __init__(
        self,
        component_id: int,
        position: Position,
        min_text: str,
        max_text: str,
        value_text: str,
        rounding_text: str,
    ):
        super().__init__(ComponentType.PropertySlider, component_id, position, 0.5, min_text, max_text, value_text=value_text)
        self.rounding_text: str = rounding_text

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertySlider:
        assert element.tag == 'c', f'invalid PropertySlider {element}'
        assert element.attributes.get('type', '0') == str(ComponentType.PropertySlider.value), f'Not an PropertySlider {element}'
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = PropertySlider._basic_in_parsing(obj)
        min_text, max_text = PropertySlider._basic_min_max_parsing(obj)
        value_text: str = PropertySlider._basic_value_parsing(obj)
        rounding_text: str = PropertySlider._basic_number_field_parsing(obj, 'int')
        return PropertySlider(component_id, position, min_text, max_text, value_text, rounding_text)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml({})
        children.extend(self._min_max_to_xml())
        children.extend(self._value_to_xml())
        children.append(self._to_xml_number_field('int', self.rounding_text))
        return {}, children

    @property
    def rounding(self) -> float:
        return string_to_sw_float(self.rounding_text)

    @rounding.setter
    def rounding(self, value: float):
        self.rounding_text = str(value)
