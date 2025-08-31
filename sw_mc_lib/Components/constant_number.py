from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class ConstantNumber(Component):
    """
    Outputs a constant number that is set on the properties panel.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        value_property: Optional[NumberProperty] = None,
    ):
        super().__init__(ComponentType.ConstantNumber, component_id, position, 0.5)
        self.value_property: NumberProperty = value_property or NumberProperty("0", "n")

    @staticmethod
    def from_xml(element: XMLParserElement) -> ConstantNumber:
        obj: XMLParserElement = element.children[0]
        component_id, position, _, properties = Component._basic_in_parsing(obj)
        return ConstantNumber(component_id, position, properties.get("n"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(properties={"n": self.value_property})
