from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class VideoSwitchbox(Component):
    """
    Outputs the first input video when receiving an on signal, and the second when receiving an off signal.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        on_value_input: Optional[Input] = None,
        off_value_input: Optional[Input] = None,
        switch_signal_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.VideoSwitchbox, component_id, position, 1.0)
        self.on_value_input: Optional[Input] = on_value_input
        self.off_value_input: Optional[Input] = off_value_input
        self.switch_signal_input: Optional[Input] = switch_signal_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> VideoSwitchbox:
        assert element.tag == "c", f"invalid VideoSwitchbox {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.VideoSwitchbox.value
        ), f"Not an VideoSwitchbox {element}"
        obj: XMLParserElement = element.children[0]
        (
            component_id,
            position,
            inputs,
            _,
        ) = VideoSwitchbox._basic_in_parsing(obj)
        return VideoSwitchbox(
            component_id, position, inputs.get("1"), inputs.get("2"), inputs.get("3")
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(
            self.on_value_input, self.off_value_input, self.switch_signal_input
        )
