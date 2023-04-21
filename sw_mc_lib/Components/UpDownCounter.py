from __future__ import annotations

from typing import Optional

from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.util import string_to_sw_float
from .SubTypes.ResetComponent import ResetComponent
from .SubTypes.MinMaxComponent import MinMaxComponent


class UpDownCounter(MinMaxComponent, ResetComponent):
    def __init__(
        self,
        component_id: int,
        position: Position,
        up: Optional[int],
        down: Optional[int],
        reset: Optional[int],
        min_text: str,
        max_text: str,
        reset_text: str,
        increment_text: str,
    ):
        super().__init__(ComponentType.UpDownCounter, component_id, position, 1.0, min_text, max_text, reset_text=reset_text)
        self.up: Optional[int] = up
        self.down: Optional[int] = down
        self.reset: Optional[int] = reset
        self.increment_text: str = increment_text

    @staticmethod
    def from_xml(element: XMLParserElement) -> UpDownCounter:
        assert element.tag == 'c', f'invalid UpDownCounter {element}'
        assert element.attributes.get('type', '0') == str(
            ComponentType.UpDownCounter.value
            ), f'Not an UpDownCounter {element}'
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = UpDownCounter._basic_in_parsing(obj)
        min_text, max_text = UpDownCounter._basic_min_max_parsing(obj)
        reset_text = UpDownCounter._basic_reset_parsing(obj)
        increment_text: str = UpDownCounter._basic_number_field_parsing(obj, 'i')
        return UpDownCounter(component_id, position, inputs.get(1), inputs.get(2), inputs.get(3), min_text, max_text, reset_text, increment_text)

    def _inner_to_xml(self) -> str:
        xml: str = self.indent(self._pos_in_to_xml({1: self.up, 2: self.down, 3: self.reset}))
        xml += self.indent(self._to_xml_number_field('i', self.increment_text))
        xml += self.indent(self._min_max_to_xml())
        xml += self.indent(self._reset_to_xml())
        return xml

    @property
    def increment(self) -> float:
        return string_to_sw_float(self.increment_text)

    @increment.setter
    def increment(self, value: float):
        self.increment_text = str(value)
