from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement

from .SubTypes.MinMaxComponent import MinMaxComponent


class Clamp(MinMaxComponent):
    """
    Clamps the input value between a set min and max and outputs the result.
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
            ComponentType.Clamp, component_id, position, 0.5, min_property, max_property
        )
        self.number_input: Optional[Input] = number_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> Clamp:
        assert element.tag == "c", f"invalid Clamp {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Clamp.value
        ), f"Not an Clamp {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Clamp._basic_in_parsing(obj)
        min_property, max_property = Clamp._basic_min_max_parsing(properties)
        return Clamp(
            component_id, position, min_property, max_property, inputs.get("1")
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml(self.number_input)
        children.extend(self._min_max_to_xml())
        return {}, children
