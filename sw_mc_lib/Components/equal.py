from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberInput, NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class Equal(Component):
    """
    Compares whether or not two numbers are equal within a set accuracy.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        a_input: Optional[Input] = None,
        b_input: Optional[Input] = None,
        epsilon_property: NumberInput = None,
    ):
        super().__init__(ComponentType.Equal, component_id, position)
        self.a_input: Optional[Input] = a_input
        self.b_input: Optional[Input] = b_input
        self.epsilon_property: NumberProperty = NumberProperty.from_input(
            epsilon_property, "e", "0.0001"
        )

    @property
    def height(self) -> float:
        return 0.75

    @staticmethod
    def from_xml(element: XMLParserElement) -> Equal:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Component._basic_in_parsing(obj)
        return Equal(
            component_id,
            position,
            inputs.get("1"),
            inputs.get("2"),
            properties.get("e"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(
            self.a_input, self.b_input, properties={"e": self.epsilon_property}
        )
