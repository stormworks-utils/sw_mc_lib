from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class CompositeBinaryToNumber(Component):
    """
    Reads the on/off signals of a composite link and encodes them in the bits of an output number.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        signal_to_convert_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.CompositeBinaryToNumber, component_id, position)
        self.signal_to_convert_input: Optional[Input] = signal_to_convert_input

    @property
    def height(self) -> float:
        return 0.5

    @staticmethod
    def from_xml(element: XMLParserElement) -> CompositeBinaryToNumber:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = Component._basic_in_parsing(obj)
        return CompositeBinaryToNumber(component_id, position, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.signal_to_convert_input)
