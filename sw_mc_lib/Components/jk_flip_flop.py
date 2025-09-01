from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class JKFlipFlop(Component):
    """
    An JK flip flop that can be set and reset using two on/off inputs.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        set_input: Optional[Input] = None,
        reset_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.JKFlipFlop, component_id, position)
        self.set_input: Optional[Input] = set_input
        self.reset_input: Optional[Input] = reset_input

    @property
    def height(self) -> float:
        return 0.75

    @staticmethod
    def from_xml(element: XMLParserElement) -> JKFlipFlop:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = Component._basic_in_parsing(obj)
        return JKFlipFlop(component_id, position, inputs.get("1"), inputs.get("2"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.set_input, self.reset_input)
