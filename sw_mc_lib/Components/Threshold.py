from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class Threshold(Component):
    """
    Outputs an on/off signal indicating whether or not the input value is within a set threshold.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        min_property: Optional[NumberProperty] = None,
        max_property: Optional[NumberProperty] = None,
        number_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.Threshold, component_id, position, 0.5)
        self.number_input: Optional[Input] = number_input
        self.min_property: NumberProperty = min_property or NumberProperty("0", "min")
        self.max_property: NumberProperty = max_property or NumberProperty("0", "max")

    @staticmethod
    def from_xml(element: XMLParserElement) -> Threshold:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Component._basic_in_parsing(obj)
        return Threshold(
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
