from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class NumericalJunction(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        value_to_pass_through: Optional[Input],
        switch_signal: Optional[Input],
    ):
        super().__init__(ComponentType.NumericalJunction, component_id, position, 0.75)
        self.value_to_pass_through: Optional[Input] = value_to_pass_through
        self.switch_signal: Optional[Input] = switch_signal

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
            properties,
        ) = NumericalJunction._basic_in_parsing(obj)
        return NumericalJunction(
            component_id, position, inputs.get("1"), inputs.get("2")
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.value_to_pass_through, self.switch_signal)
