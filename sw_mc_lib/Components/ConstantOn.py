from __future__ import annotations

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class ConstantOn(Component):
    """
    Outputs a constant on signal.
    """

    def __init__(self, component_id: int, position: Position):
        super().__init__(ComponentType.ConstantOn, component_id, position, 0.5)

    @staticmethod
    def from_xml(element: XMLParserElement) -> ConstantOn:
        assert element.tag == "c", f"invalid ConstantOn {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.ConstantOn.value
        ), f"Not an ConstantOn {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, _, _ = ConstantOn._basic_in_parsing(obj)
        return ConstantOn(component_id, position)

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml()
