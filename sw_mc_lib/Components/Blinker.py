from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class Blinker(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        control_signal: Optional[int],
        blink_on_duration: float,
        blink_off_duration: float,
    ):
        super().__init__(ComponentType.Blinker, component_id, position, 1.0)
        self.control_signal: Optional[int] = control_signal
        self.blink_on_duration: float = blink_on_duration
        self.blink_off_duration: float = blink_off_duration

    @staticmethod
    def from_xml(element: XMLParserElement) -> Blinker:
        assert element.tag == 'c', f'invalid Blinker {element}'
        assert element.attributes.get('type', '0') == str(
            ComponentType.Blinker.value
            ), f'Not an Blinker {element}'
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = Blinker._basic_in_parsing(obj)
        blink_on_duration: float = float(obj.attributes.get('on', '1'))
        blink_off_duration: float = float(obj.attributes.get('off', '1'))
        return Blinker(component_id, position, inputs.get(1), blink_on_duration, blink_off_duration)

    def _inner_to_xml(self) -> str:
        xml: str = f'on="{self.blink_on_duration}" off="{self.blink_off_duration}"\n'
        xml += self.indent(self._pos_in_to_xml({1: self.control_signal}))
        return xml
