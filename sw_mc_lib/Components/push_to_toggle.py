from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class PushToToggle(Component):
    """
    An on/off switch that is toggled every time a new on signal is sent to its input.
    """

    def __init__(
        self, component_id: int, position: Position, a_input: Optional[Input] = None
    ):
        super().__init__(ComponentType.PushToToggle, component_id, position)
        self.a_input: Optional[Input] = a_input

    @property
    def height(self) -> float:
        return 0.5

    @staticmethod
    def from_xml(element: XMLParserElement) -> PushToToggle:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = Component._basic_in_parsing(obj)
        return PushToToggle(component_id, position, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.a_input)
