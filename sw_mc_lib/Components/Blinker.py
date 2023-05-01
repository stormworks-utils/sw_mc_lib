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
        super().__init__(ComponentType.Blinker, component_id, position, 1.0)
        self.control_signal_input: Optional[Input] = control_signal_input
        self.blink_on_duration_property: float = blink_on_duration_property
        self.blink_off_duration_property: float = blink_off_duration_property

    @staticmethod
    def from_xml(element: XMLParserElement) -> Blinker:
        assert element.tag == "c", f"invalid Blinker {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Blinker.value
        ), f"Not an Blinker {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = Blinker._basic_in_parsing(obj)
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
        attributes: dict[str, str] = {
            "on": str(self.blink_on_duration_property),
            "off": str(self.blink_off_duration_property),
        }
        children: list[XMLParserElement] = self._pos_in_to_xml(
            self.control_signal_input
        )
        return attributes, children
