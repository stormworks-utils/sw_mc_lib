from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class Blinker(Component):
    """
    Outputs a value that blinks between on and off at a set rate.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        control_signal_input: Optional[Input] = None,
        blink_on_duration_property: float = 1.0,
        blink_off_duration_property: float = 1.0,
    ):
        super().__init__(ComponentType.Blinker, component_id, position)
        self.control_signal_input: Optional[Input] = control_signal_input
        self.blink_on_duration_property: float = blink_on_duration_property
        self.blink_off_duration_property: float = blink_off_duration_property

    @property
    def height(self) -> float:
        return 0.5

    @staticmethod
    def from_xml(element: XMLParserElement) -> Blinker:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = Component._basic_in_parsing(obj)
        blink_on_duration_property: float = float(obj.attributes.get("on", "1"))
        blink_off_duration_property: float = float(obj.attributes.get("off", "1"))
        return Blinker(
            component_id,
            position,
            inputs.get("1"),
            blink_on_duration_property,
            blink_off_duration_property,
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {
            "on": str(self.blink_on_duration_property),
            "off": str(self.blink_off_duration_property),
        }, self._pos_in_to_xml(self.control_signal_input)
