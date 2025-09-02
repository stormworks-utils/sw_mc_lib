from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberInput, NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class Clamp(Component):
    """
    Clamps the input value between a set min and max and outputs the result.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        min_property: NumberInput = None,
        max_property: NumberInput = None,
        number_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.Clamp, component_id, position)
        self.number_input: Optional[Input] = number_input
        self.min_property: NumberProperty = NumberProperty.from_input(
            min_property, "min"
        )
        self.max_property: NumberProperty = NumberProperty.from_input(
            max_property, "max"
        )

    @property
    def height(self) -> float:
        return 0.5

    @staticmethod
    def from_xml(element: XMLParserElement) -> Clamp:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Component._basic_in_parsing(obj)
        return Clamp(
            component_id,
            position,
            properties.get("min"),
            properties.get("max"),
            inputs.get("1"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(
            self.number_input,
            properties={"min": self.min_property, "max": self.max_property},
        )
