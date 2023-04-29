from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class Blinker(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        control_signal: Optional[Input],
        blink_on_duration: float,
        blink_off_duration: float,
    ):
        super().__init__(ComponentType.Blinker, component_id, position, 1.0)
        self.control_signal: Optional[Input] = control_signal
        self.blink_on_duration: float = blink_on_duration
        self.blink_off_duration: float = blink_off_duration

    @staticmethod
    def from_xml(element: XMLParserElement) -> Blinker:
        assert element.tag == "c", f"invalid Blinker {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Blinker.value
        ), f"Not an Blinker {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Blinker._basic_in_parsing(obj)
        blink_on_duration: float = float(obj.attributes.get("on", "1"))
        blink_off_duration: float = float(obj.attributes.get("off", "1"))
        return Blinker(
            component_id,
            position,
            inputs.get("1"),
            blink_on_duration,
            blink_off_duration,
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {
            "on": str(self.blink_on_duration),
            "off": str(self.blink_off_duration),
        }
        children: list[XMLParserElement] = self._pos_in_to_xml(self.control_signal)
        return attributes, children
