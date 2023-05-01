from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class NumberToCompositeBinary(Component):
    """
    Converts a number (rounded) to binary and outputs the bits as composite on/off signals.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        number_to_convert_input: Optional[Input] = None,
    ):
        super().__init__(
            ComponentType.NumberToCompositeBinary, component_id, position, 0.5
        )
        self.number_to_convert_input: Optional[Input] = number_to_convert_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> NumberToCompositeBinary:
        assert element.tag == "c", f"invalid NumberToCompositeBinary {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.NumberToCompositeBinary.value
        ), f"Not an NumberToCompositeBinary {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = NumberToCompositeBinary._basic_in_parsing(
            obj
        )
        return NumberToCompositeBinary(component_id, position, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.number_to_convert_input)
