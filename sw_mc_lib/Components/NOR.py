from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class NOR(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        a: Optional[Input],
        b: Optional[Input],
    ):
        super().__init__(ComponentType.NOR, component_id, position, 0.75)
        self.a: Optional[Input] = a
        self.b: Optional[Input] = b

    @staticmethod
    def from_xml(element: XMLParserElement) -> NOR:
        assert element.tag == "c", f"invalid NOR {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.NOR.value
        ), f"Not an NOR {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = NOR._basic_in_parsing(obj)
        return NOR(component_id, position, inputs.get("1"), inputs.get("2"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.a, self.b)
