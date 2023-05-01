from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class NumericalJunction(Component):
    """
    Outputs the input number to one of the outputs depending on whether or not the Switch Signal is on.
    The path that the input doesn't take will output a value of 0.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        value_to_pass_through_input: Optional[Input] = None,
        switch_signal_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.NumericalJunction, component_id, position, 0.75)
        self.value_to_pass_through_input: Optional[Input] = value_to_pass_through_input
        self.switch_signal_input: Optional[Input] = switch_signal_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> NumericalJunction:
        assert element.tag == "c", f"invalid NumericalJunction {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.NumericalJunction.value
        ), f"Not an NumericalJunction {element}"
        obj: XMLParserElement = element.children[0]
        (
            component_id,
            position,
            inputs,
            _,
        ) = NumericalJunction._basic_in_parsing(obj)
        return NumericalJunction(
            component_id, position, inputs.get("1"), inputs.get("2")
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(
            self.value_to_pass_through_input, self.switch_signal_input
        )
