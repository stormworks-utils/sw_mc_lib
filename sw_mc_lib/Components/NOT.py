from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class NOT(Component):
    def __init__(self, component_id: int, position: Position, a: Optional[Input]):
        super().__init__(ComponentType.NOT, component_id, position, 0.5)
        self.a: Optional[Input] = a

    @staticmethod
    def from_xml(element: XMLParserElement) -> NOT:
        assert element.tag == "c", f"invalid NOT {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.NOT.value
        ), f"Not an NOT {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = NOT._basic_in_parsing(obj)
        return NOT(component_id, position, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.a)
