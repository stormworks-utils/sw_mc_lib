from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class Abs(Component):
    """
    Outputs the absolute value of the input value (negative numbers become positive).
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        number_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.Abs, component_id, position, 0.5)
        self.number_input: Optional[Input] = number_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> Abs:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = Component._basic_in_parsing(obj)
        return Abs(component_id, position, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.number_input)
