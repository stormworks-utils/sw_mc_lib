from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType, PulseMode
from sw_mc_lib.XMLParser import XMLParserElement


class Pulse(Component):
    """
    A switch that outputs a single tick pulse.
    It can be configured to pulse when being switched from off to on (default), on to off,
    or always when the input signal changes.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        mode_property: PulseMode = PulseMode.OffToOn,
        toggle_signal_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.Pulse, component_id, position, 0.5)
        self.toggle_signal_input: Optional[Input] = toggle_signal_input
        self.mode_property: PulseMode = mode_property

    @staticmethod
    def from_xml(element: XMLParserElement) -> Pulse:
        assert element.tag == "c", f"invalid Pulse {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Pulse.value
        ), f"Not an Pulse {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = Pulse._basic_in_parsing(obj)
        mode_property: PulseMode = PulseMode(int(obj.attributes.get("m", "1")))
        return Pulse(component_id, position, mode_property, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {"m": str(self.mode_property.value)}, self._pos_in_to_xml(
            self.toggle_signal_input
        )
