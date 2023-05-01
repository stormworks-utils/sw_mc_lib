from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement

from .SubTypes.MinMaxComponent import MinMaxComponent


class Threshold(MinMaxComponent):
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
        super().__init__(
            ComponentType.Threshold,
            component_id,
            position,
            0.5,
            min_property,
            max_property,
        )
        self.number_input: Optional[Input] = number_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> Threshold:
        assert element.tag == "c", f"invalid Threshold {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Threshold.value
        ), f"Not an Threshold {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Threshold._basic_in_parsing(obj)
        min_property, max_property = Threshold._basic_min_max_parsing(properties)
        return Threshold(
            component_id, position, min_property, max_property, inputs.get("1")
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml(self.number_input)
        children.extend(self._min_max_to_xml())
        return {}, children
