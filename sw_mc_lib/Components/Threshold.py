from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberProperty
from .SubTypes.MinMaxComponent import MinMaxComponent


class Threshold(MinMaxComponent):
    def __init__(
        self,
        component_id: int,
        position: Position,
        min: NumberProperty,
        max: NumberProperty,
        input_number: Optional[Input],
    ):
        super().__init__(ComponentType.Threshold, component_id, position, 0.5, min, max)
        self.input_number: Optional[Input] = input_number

    @staticmethod
    def from_xml(element: XMLParserElement) -> Threshold:
        assert element.tag == "c", f"invalid Threshold {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Threshold.value
        ), f"Not an Threshold {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Threshold._basic_in_parsing(obj)
        min, max = Threshold._basic_min_max_parsing(properties)
        return Threshold(component_id, position, min, max, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml(self.input_number)
        children.extend(self._min_max_to_xml())
        return {}, children
